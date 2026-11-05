"""Nodo camarero: recibe pedidos por mesa y lleva el robot con Nav2.

Interfaz (relativa al namespace del robot, p. ej. /rosbot2r/...):
  Suscribe  camarero/pedido     std_msgs/String  "mesa_3", "3" o "cocina"
  Suscribe  camarero/entregado  std_msgs/Empty   el cliente ha recogido el plato
  Suscribe  camarero/cancelar   std_msgs/Empty   para y vacía la cola
  Publica   camarero/estado     std_msgs/String  JSON {estado, destino, cola, detalle}
  Usa       navigate_to_pose    nav2_msgs/action/NavigateToPose

Ciclo: EN_BASE -> YENDO_A_MESA -> EN_MESA (espera 'entregado' o timeout)
       -> VOLVIENDO -> EN_BASE -> (siguiente pedido de la cola)
"""

import json
from collections import deque

import rclpy
from action_msgs.msg import GoalStatus
from geometry_msgs.msg import PoseStamped
from nav2_msgs.action import NavigateToPose
from rclpy.action import ActionClient
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from rclpy.qos import DurabilityPolicy, QoSProfile
from std_msgs.msg import Empty, String

from camarero.mesas import cargar_mesas, normalizar_destino

EN_BASE = "EN_BASE"
YENDO_A_MESA = "YENDO_A_MESA"
EN_MESA = "EN_MESA"
VOLVIENDO = "VOLVIENDO"
ESPERANDO_SALIDA = "ESPERANDO_SALIDA"
PARADO = "PARADO"
ERROR = "ERROR"


class Camarero(Node):
    def __init__(self):
        super().__init__("camarero")
        ruta = self.declare_parameter("mesas_file", "/camarero/config/mesas_sim.yaml").value
        self.espera_en_mesa = float(self.declare_parameter("espera_en_mesa_s", 60.0).value)
        self.espera_en_base = float(self.declare_parameter("espera_en_base_s", 5.0).value)

        self.frame_id, self.base, self.poses = cargar_mesas(ruta)
        self.get_logger().info(
            f"Mesas cargadas de {ruta}: {', '.join(self.poses)} (base={self.base}, frame={self.frame_id})"
        )

        self.cola = deque()
        self.estado = EN_BASE
        self.destino = None
        self.goal_handle = None
        self.temporizador = None
        self.secuencia = 0  # invalida callbacks de objetivos antiguos

        self.nav = ActionClient(self, NavigateToPose, "navigate_to_pose")
        latched = QoSProfile(depth=1, durability=DurabilityPolicy.TRANSIENT_LOCAL)
        self.pub_estado = self.create_publisher(String, "camarero/estado", latched)
        self.create_subscription(String, "camarero/pedido", self.on_pedido, 10)
        self.create_subscription(Empty, "camarero/entregado", self.on_entregado, 10)
        self.create_subscription(Empty, "camarero/cancelar", self.on_cancelar, 10)
        self.publicar("Listo para recibir pedidos")

    # ---------- entradas ----------
    def on_pedido(self, msg):
        nombre = normalizar_destino(msg.data, self.poses)
        if nombre is None:
            self.get_logger().warning(f"Destino desconocido: '{msg.data}'")
            self.publicar(f"Destino desconocido: {msg.data}")
            return
        if nombre == self.base:
            self.cancelar_timer()
            self.cola.clear()
            self.navegar(self.base, VOLVIENDO)
            return
        self.cola.append(nombre)
        self.get_logger().info(f"Pedido para {nombre}; cola={list(self.cola)}")
        if self.estado in (EN_BASE, PARADO, ERROR):
            self.siguiente()
        else:
            self.publicar(f"Pedido {nombre} en cola")

    def on_entregado(self, _msg):
        if self.estado != EN_MESA:
            self.publicar("'entregado' ignorado: el robot no está en una mesa")
            return
        self.cancelar_timer()
        self.publicar(f"Entregado en {self.destino}")
        self.navegar(self.base, VOLVIENDO)

    def on_cancelar(self, _msg):
        self.cola.clear()
        self.cancelar_timer()
        self.secuencia += 1
        if self.goal_handle is not None:
            self.goal_handle.cancel_goal_async()
            self.goal_handle = None
        self.estado = PARADO
        self.publicar("Cancelado por el usuario; cola vaciada")

    # ---------- lógica ----------
    def siguiente(self):
        self.cancelar_timer()
        if not self.cola:
            self.estado = EN_BASE
            self.destino = self.base
            self.publicar("En base, sin pedidos")
            return
        self.navegar(self.cola.popleft(), YENDO_A_MESA)

    def navegar(self, nombre, estado):
        if not self.nav.wait_for_server(timeout_sec=2.0):
            self.estado = ERROR
            self.publicar("Nav2 no responde (navigate_to_pose)")
            return
        if self.goal_handle is not None:
            self.goal_handle.cancel_goal_async()
            self.goal_handle = None

        pose = self.poses[nombre]
        goal = NavigateToPose.Goal()
        goal.pose = PoseStamped()
        goal.pose.header.frame_id = self.frame_id
        goal.pose.header.stamp = self.get_clock().now().to_msg()
        goal.pose.pose.position.x = pose.x
        goal.pose.pose.position.y = pose.y
        q = pose.quaternion()
        goal.pose.pose.orientation.x, goal.pose.pose.orientation.y = q[0], q[1]
        goal.pose.pose.orientation.z, goal.pose.pose.orientation.w = q[2], q[3]

        self.secuencia += 1
        seq = self.secuencia
        self.estado, self.destino = estado, nombre
        self.publicar(f"Navegando a {nombre}")
        self.nav.send_goal_async(goal).add_done_callback(lambda f: self.on_goal_aceptado(f, seq))

    def on_goal_aceptado(self, futuro, seq):
        if seq != self.secuencia:
            return
        handle = futuro.result()
        if not handle.accepted:
            self.estado = ERROR
            self.publicar(f"Nav2 rechazó el objetivo {self.destino}")
            return
        self.goal_handle = handle
        handle.get_result_async().add_done_callback(lambda f: self.on_resultado(f, seq))

    def on_resultado(self, futuro, seq):
        if seq != self.secuencia:
            return
        self.goal_handle = None
        status = futuro.result().status
        if status != GoalStatus.STATUS_SUCCEEDED:
            self.estado = ERROR
            self.publicar(f"No se pudo llegar a {self.destino} (status {status})")
            return
        if self.estado == YENDO_A_MESA:
            self.estado = EN_MESA
            self.publicar(f"En {self.destino}, esperando recogida")
            self.temporizador = self.create_timer(self.espera_en_mesa, self.timeout_mesa)
        else:  # VOLVIENDO
            self.estado = EN_BASE
            if self.cola:
                self.estado = ESPERANDO_SALIDA
                self.publicar(f"En base; sale hacia {self.cola[0]} en {self.espera_en_base:.0f} s")
                self.temporizador = self.create_timer(self.espera_en_base, self.siguiente)
            else:
                self.siguiente()

    def timeout_mesa(self):
        self.cancelar_timer()
        self.publicar(f"Sin confirmación en {self.destino} tras {self.espera_en_mesa:.0f} s; vuelve")
        self.navegar(self.base, VOLVIENDO)

    def cancelar_timer(self):
        if self.temporizador is not None:
            self.temporizador.cancel()
            self.destroy_timer(self.temporizador)
            self.temporizador = None

    def publicar(self, detalle):
        datos = {"estado": self.estado, "destino": self.destino, "cola": list(self.cola), "detalle": detalle}
        self.pub_estado.publish(String(data=json.dumps(datos, ensure_ascii=False)))
        self.get_logger().info(f"[{self.estado}] {detalle}")


def main():
    rclpy.init()
    nodo = Camarero()
    try:
        rclpy.spin(nodo)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass  # Ctrl+C o 'docker stop'
    finally:
        nodo.destroy_node()
        rclpy.try_shutdown()


if __name__ == "__main__":
    main()
