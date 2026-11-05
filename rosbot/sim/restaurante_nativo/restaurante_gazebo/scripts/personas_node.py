#!/usr/bin/env python3
# Autora: Irene González
"""Mueve las "personas" del escenario por sus rutas (ida y vuelta, en bucle).

Cada persona es un modelo de Gazebo con VelocityControl y PosePublisher. A través de ros_gz_bridge:
    /model/<nombre>/pose     (geometry_msgs/Pose, Gazebo -> ROS)  posición actual en el frame world
    /model/<nombre>/cmd_vel  (geometry_msgs/Twist, ROS -> Gazebo) velocidad en el frame del modelo

Parámetros:
    escenarios_file (str): ruta a config/escenarios.yaml
    escenario (str): nombre del escenario
"""

import math

import rclpy
import yaml
from geometry_msgs.msg import Pose, Twist
from rclpy.node import Node

TOLERANCIA = 0.05  # m: se considera alcanzado el punto de la ruta
FRECUENCIA = 20.0  # Hz del bucle de control


def yaw_de(q):
    return math.atan2(2.0 * (q.w * q.z + q.x * q.y), 1.0 - 2.0 * (q.y * q.y + q.z * q.z))


class Persona:
    def __init__(self, node, cfg):
        self.nombre = cfg["nombre"]
        self.velocidad = float(cfg["velocidad"])
        self.pausa = float(cfg.get("pausa", 0.0))
        ruta = [tuple(p) for p in cfg["ruta"]]
        # Ida y vuelta: A B C -> A B C B (y vuelve a A). Con dos puntos: A B.
        self.ruta = ruta + ruta[-2:0:-1] if len(ruta) > 2 else ruta
        self.objetivo = 1 % len(self.ruta)
        self.pose = None
        self.fin_pausa = None
        self.pub = node.create_publisher(Twist, f"/model/{self.nombre}/cmd_vel", 10)
        node.create_subscription(Pose, f"/model/{self.nombre}/pose", self._pose_cb, 10)

    def _pose_cb(self, msg):
        self.pose = msg

    def paso(self, ahora):
        cmd = Twist()
        if self.pose is None or len(self.ruta) < 2:
            self.pub.publish(cmd)
            return
        if self.fin_pausa is not None:
            if ahora < self.fin_pausa:
                self.pub.publish(cmd)
                return
            self.fin_pausa = None
        tx, ty = self.ruta[self.objetivo]
        dx, dy = tx - self.pose.position.x, ty - self.pose.position.y
        dist = math.hypot(dx, dy)
        if dist < TOLERANCIA:
            self.objetivo = (self.objetivo + 1) % len(self.ruta)
            if self.pausa > 0:
                self.fin_pausa = ahora + self.pausa
            self.pub.publish(cmd)
            return
        v = min(self.velocidad, dist * FRECUENCIA)  # no pasarse del punto en el último paso
        vx, vy = v * dx / dist, v * dy / dist
        # VelocityControl usa el frame del modelo: girar la velocidad según el yaw actual.
        yaw = yaw_de(self.pose.orientation)
        c, s = math.cos(yaw), math.sin(yaw)
        cmd.linear.x = c * vx + s * vy
        cmd.linear.y = -s * vx + c * vy
        self.pub.publish(cmd)


class PersonasNode(Node):
    def __init__(self):
        super().__init__("personas_node")
        archivo = self.declare_parameter("escenarios_file", "").value
        escenario = self.declare_parameter("escenario", "vacio").value
        with open(archivo, encoding="utf-8") as f:
            esc = yaml.safe_load(f)["escenarios"][escenario]
        self.personas = [Persona(self, p) for p in esc.get("personas") or []]
        nombres = ", ".join(p.nombre for p in self.personas) or "ninguna"
        self.get_logger().info(f"Escenario '{escenario}': personas = {nombres}")
        self.create_timer(1.0 / FRECUENCIA, self._bucle)
        self._avisado = False

    def _bucle(self):
        ahora = self.get_clock().now().nanoseconds * 1e-9
        for p in self.personas:
            p.paso(ahora)
        if not self._avisado and ahora > 20.0:
            sin_pose = [p.nombre for p in self.personas if p.pose is None]
            if sin_pose:
                self.get_logger().warn(f"No llega la posición de: {', '.join(sin_pose)} (¿bridge?)")
            self._avisado = True


def main():
    rclpy.init()
    node = PersonasNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        for p in node.personas:
            p.pub.publish(Twist())
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == "__main__":
    main()
