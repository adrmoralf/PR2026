# 📋 Información del Proyecto — PR2026

## Descripción

Proyecto de robótica inspirado en los **restaurantes de sushi con gatos robot** 🐱🍣. El objetivo es desarrollar un robot camarero autónomo capaz de llevar platos desde la cocina hasta las mesas de los clientes.

- **Robot:** ROSbot 2 PRO (Husarion), unidad comprobada con placa UP Board, Ubuntu 20.04.6 x86-64 y ROS 2 Humble en contenedores Docker. El sistema anfitrión también tiene ROS 2 Foxy; las herramientas de integración deben ejecutarse en Humble, que es donde está el stack activo.
- **Automatización:** Node-RED como orquestador central para gestionar la lógica de pedidos, rutas y estado del robot.
- **Pedidos:** Los clientes (cada integrante con su móvil) hacen pedidos a través de un **bot de Telegram**, que se comunica con Node-RED.

### Flujo general

```
Cliente (Telegram) → Bot Telegram → Node-RED → rosbridge/WebSocket → Nav2 → ROSbot → Mesa → confirmación Telegram
```

Node-RED mantendrá el pedido y su estado; Nav2 planificará y ejecutará el desplazamiento. El bot no conducirá las ruedas con comandos de velocidad: convertirá una mesa validada en una pose de destino conocida en el mapa.

## 👥 Integrantes

| Nombre | Archivo de notas |
|--------|-----------------|
| Adri   | [Adri.md](Adri.md) |
| Manu   | [Manu.md](Manu.md) |
| Rubén  | [Ruben.md](Ruben.md) |
| Irene  | [Irene.md](Irene.md) |

## 🎯 Objetivos

1. Mantener la integración alineada con ROS 2 Humble, distribución observada en los contenedores activos del robot; no asumir que el ROS 2 Foxy del host es el entorno de navegación.
2. Implementar **navegación autónoma** (SLAM, localización, planificación de rutas) para que el robot se desplace entre cocina y mesas.
3. Crear un **bot de Telegram** para que los clientes hagan pedidos desde su móvil.
4. Desarrollar flujos en **Node-RED** que conecten los pedidos de Telegram con las órdenes de movimiento del robot.
5. Definir un **mapa del restaurante** con las posiciones de las mesas y la cocina.
6. Integrar todo el sistema: pedido → procesamiento → navegación → entrega.
7. Documentar todo el proceso y errores encontrados.

## 🗓️ Entregas

| Entrega | Fecha límite | Descripción | Estado |
|---------|-------------|-------------|--------|
| _Pendiente de definir_ | — | — | ⬜ |

> **Nota:** Actualizar esta tabla a medida que se conozcan las fechas y requisitos de cada entrega.

## 🛠️ Tecnologías

| Componente | Tecnología |
|------------|-----------|
| **Robot** | ROSbot 2 PRO (Husarion) |
| **Framework robótico** | ROS 2 (distribución por confirmar tras inspeccionar la imagen del ROSbot 2 PRO) |
| **Navegación** | Nav2 (Navigation Stack 2) |
| **Automatización / Orquestador** | Node-RED |
| **Interfaz de pedidos** | Bot de Telegram |
| **Lenguajes** | Python / C++ (ROS2), JavaScript (Node-RED) |
| **SO** | Ubuntu (Linux) |

## 🍽️ Flujo funcional del robot camarero

1. El cliente abre el bot de Telegram, elige mesa y productos mediante botones/lista controlada. Evitar texto libre para la mesa: se valida contra el catálogo de mesas.
2. Node-RED valida usuario/chat autorizado, mesa, productos y disponibilidad del robot. Crea un identificador único de pedido y responde que lo recibió (sin afirmar todavía que salió o llegó).
3. El pedido pasa a una cola persistente con estados sugeridos: `recibido`, `pendiente`, `en_camino`, `llegado`, `entregado`, `cancelado` y `error`. Se debe impedir procesar dos veces el mismo update/pedido.
4. Node-RED consulta el catálogo local mesa→pose y envía un goal `NavigateToPose` con posición y orientación en el frame `map`.
5. Nav2 planifica y mueve el robot usando el mapa/localización/sensores. Node-RED escucha aceptación, feedback y resultado; comunica llegada o fallo por Telegram.
6. En la mesa, el cliente o personal confirma la entrega desde Telegram/botón físico; entonces se marca `entregado` y se procesa el siguiente pedido (o retorno a cocina/estación de espera según política).

### Componentes y responsabilidades

| Componente | Responsabilidad | Despliegue previsto |
|---|---|---|
| Bot de Telegram | Interfaz de pedidos y avisos al usuario | Integrado en Node-RED; usar nodo para **Bot API**, no un nodo de cuenta personal/userbot |
| Node-RED | Validación, catálogo de mesas, cola, estados, reglas de operación y avisos | Contenedor aparte en laptop/PC; puerto `1880`, volumen persistente `/data` |
| rosbridge_suite | Puente JSON/WebSocket hacia interfaces ROS 2 | En el grafo ROS 2 Humble del robot, WebSocket normalmente en `9090` |
| Nav2 (`rosbot-autonomy`) | Localización, planificación, navegación a destinos y resultado | Stack de autonomía oficial del ROSbot 2 PRO |
| ROSbot | Base móvil, LiDAR, odometría, IMU y ejecución física | Contenedores del robot |

### Integración propuesta

- Node-RED se ejecutará en un contenedor independiente en la laptop/PC, con el puerto `1880` publicado y `/data` persistente para conservar flujos y configuración.
- La navegación permanece en el stack oficial [`husarion/rosbot-autonomy`, rama `ros2router`](https://github.com/husarion/rosbot-autonomy/tree/ros2router), específico para ROSbot 2R/2 PRO. Node-RED no reemplaza ni reconstruye el paquete de movimiento.
- Node-RED se conecta a rosbridge por `ws://<IP-ROSbot>:9090`; al ejecutarlo en el robot, rosbridge debe compartir el entorno ROS 2 Humble y el descubrimiento DDS/grafo con Nav2. Node-RED no necesita instalar ROS 2 ni participar en DDS.
- Para destinos de mesa se utilizará la acción `nav2_msgs/action/NavigateToPose`, con poses guardadas y probadas en el mapa del restaurante. El protocolo rosbridge de la rama ROS 2 documenta operaciones de acciones, incluido `send_action_goal`, feedback, resultado y cancelación; hay que comprobar que la versión concreta instalada en Humble expone estas operaciones.
- `/cmd_vel` queda para teleoperación/pruebas supervisadas; no se usará como interfaz de pedidos. Un pedido aceptado debe terminar en resultado de navegación y confirmación del usuario/personal.
- Mantener Compose de Node-RED separado del Compose de movimiento para poder gestionar cada servicio de forma independiente.

### Datos que hay que preparar

- Mapa 2D del salón y cocina guardado y cargado por Nav2; ubicación inicial correcta del robot al arrancar.
- Catálogo de mesas con identificador legible y pose `{x, y, yaw}` expresada en el frame `map`. Las poses se levantan en RViz y se prueban físicamente con el robot vacío.
- Política de colas: pedidos FIFO como primer prototipo, comportamiento ante cancelación, robot ocupado, bloqueo, pérdida de Wi-Fi, objetivo no alcanzable y retorno a cocina/estación.
- Registro persistente de pedidos e identificadores procesados para evitar duplicados tras reinicios o reintentos de Telegram.
- Autorización: aceptar órdenes solo de chats/usuarios permitidos y no exponer rosbridge/Node-RED sin control de acceso. El WebSocket de rosbridge permite publicar y llamar interfaces ROS, por lo que no debe quedar abierto a redes no confiables.
- Seguridad física: pruebas iniciales con robot vacío y velocidad limitada, salón despejado, supervisión humana y acceso rápido al paro físico. No transportar comida/caliente hasta validar navegación, frenado y protocolo de entrega.

### Plan por etapas

1. Construir el mapa y probar navegación a poses de mesa en RViz con el flujo oficial de Husarion.
2. Ejecutar rosbridge en el grafo Humble; desde Node-RED verificar conectividad y, antes de conectar pedidos, probar lectura de estado y un goal controlado.
3. Crear catálogo de mesas y flujo de una sola orden de prueba; confirmar aceptación, llegada y fallo/cancelación.
4. Conectar Telegram usando un bot de prueba y lista permitida de usuarios; validar pedidos y respuestas sin transportar carga.
5. Añadir persistencia/idempotencia, cola de pedidos, recuperación tras reinicio y confirmación de entrega.
6. Realizar pruebas supervisadas en el salón vacío, después con carga inerte y solo al final con servicio real.

Estado: arquitectura documentada; Node-RED, rosbridge, mapa del restaurante, catálogo de poses y flujo de pedidos todavía no están desplegados/probados en este repositorio.

## 📂 Estructura del Repositorio

```
PR2026/
├── Notas/
│   ├── Adri.md        # Notas personales de Adri
│   ├── Manu.md        # Notas personales de Manu
│   ├── Ruben.md       # Notas personales de Rubén
│   ├── Irene.md       # Notas personales de Irene
│   ├── errores.md     # Registro de errores
│   ├── diario.md      # Diario de desarrollo
│   └── Info.md        # Este archivo
└── (código fuente por crear)
```

## 🔗 Recursos Útiles

- [ROSbot 2R / 2 PRO — Quick Start (Husarion)](https://husarion.com/tutorials/howtostart/rosbot2r-quick-start/)
- [Documentación ROS 2](https://docs.ros.org/)
- [Nav2 — Navigation Stack 2](https://docs.nav2.org/)
- [Conceptos de acciones en ROS 2 y NavigateToPose — Nav2](https://docs.nav2.org/jazzy/getting_started/navigation_concepts/ros2.html)
- [rosbridge_suite — protocolo ROS 2 (acciones, topics y servicios)](https://github.com/RobotWebTools/rosbridge_suite/blob/ros2/ROSBRIDGE_PROTOCOL.md)
- [Node-RED en Docker (puerto y persistencia `/data`)](https://nodered.org/docs/getting-started/docker)
- [Node-RED](https://nodered.org/docs/)
- [Nodo de Telegram para Bot API en Node-RED](https://flows.nodered.org/node/node-red-contrib-telegrambot)
- [Telegram Bot API](https://core.telegram.org/bots/api)

## 📝 Memoria del Proyecto

- [Memoria LaTeX (Overleaf)](https://www.overleaf.com/project/6ad0f3f618a8107fa81a76ec/share#dd594ebbde5234fac3de13eb5a6ef8c0eabac783d2ebbf31)
