# 📋 Información del Proyecto — PR2026

## Descripción

Proyecto de robótica inspirado en los **restaurantes de sushi con gatos robot** 🐱🍣. El objetivo es desarrollar un robot camarero autónomo capaz de llevar platos desde la cocina hasta las mesas de los clientes.

- **Robot:** ROSbot 2 PRO (Husarion), unidad comprobada con placa UP Board, Ubuntu 20.04.6 x86-64 y ROS 2 Humble en contenedores Docker. El sistema anfitrión también tiene ROS 2 Foxy; las herramientas de integración deben ejecutarse en Humble, que es donde está el stack activo.
- **Automatización:** Node-RED como orquestador central para gestionar la lógica de pedidos, rutas y estado del robot.
- **Pedidos:** Los clientes hacen pedidos a través de una **Telegram Mini App (Web App)** interactiva servida desde Node-RED y enlazada mediante bot de Telegram con códigos QR de mesa.
- **Persistencia:** Base de datos **SQLite** (`bar.db`) integrada en Node-RED para registrar comandas y estados.

### Flujo general

```
Cliente (QR / Telegram Web App) → Node-RED (HTTP In / SQLite) → Dashboard Cocina ("Listo") → rosbridge/WebSocket → Nav2 → ROSbot → Mesa → confirmación Telegram
```

Node-RED sirve la Web App de la carta, persiste el pedido en SQLite y gestiona su ciclo de vida. Tras ser marcado como preparado en cocina, Nav2 planificará y ejecutará el desplazamiento del ROSbot 2 PRO a la pose de la mesa.

## 👥 Integrantes

| Nombre | Archivo de notas |
|--------|-----------------|
| Adri   | [Adri.md](Adri.md) |
| Manu   | [Manu.md](Manu.md) |
| Rubén  | [Ruben.md](Ruben.md) |
| Irene  | [Irene.md](Irene.md) |

## 🎯 Objetivos

1. Mantener la integración alineada con ROS 2 Humble, distribución observada en los contenedores activos del robot; desarrollar en contenedores ROS compatibles en la laptop cuando sea posible.
2. Implementar **navegación autónoma** (SLAM, localización, planificación de rutas) para que el robot se desplace entre cocina y mesas.
3. Crear un **bot de Telegram** con **Telegram Mini App** para que los clientes elijan sus platos interactivamente desde el móvil.
4. Desarrollar flujos en **Node-RED** que conecten los pedidos de Telegram y base de datos con las órdenes de movimiento del robot.
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
| **Framework robótico** | ROS 2 Humble en contenedores Docker del robot; ROS 2 Foxy en el host del robot |
| **Navegación** | Nav2 (Navigation Stack 2) |
| **Automatización / Orquestador** | Node-RED (puerto 1880) |
| **Base de datos** | SQLite (`bar.db`) |
| **Túnel de red seguro** | Ngrok (HTTPS hacia Node-RED) |
| **Interfaz de pedidos** | Telegram Mini App (Web App HTML/CSS/JS) + Bot de Telegram |
| **Lenguajes** | Python / C++ (ROS2), JavaScript (Node-RED / Web App), SQL |
| **SO** | Ubuntu (Linux) |

## 🍽️ Flujo funcional del robot camarero

1. **Lectura de QR en mesa:** El cliente escanea el código QR de su mesa (`https://t.me/NOMBRE_BOT?start=NUMERO_MESA`), iniciando el bot de Telegram con el identificador de mesa.
2. **Apertura de la Mini App:** Node-RED inyecta el número de mesa como parámetro (`?mesa=X`) en el enlace seguro de Ngrok que abre la Web App de la carta interactiva (`GET /carta_app`).
3. **Selección y comanda:** El cliente selecciona platos (`+`/`-`), revisa el cálculo del total en el carrito flotante y pulsa "Enviar a cocina". La Web App envía el JSON vía `POST /recibir_pedido`.
4. **Persistencia y confirmación:** Node-RED inserta el registro en SQLite (`bar.db`, tabla `pedidos`, estado `pendiente`) y notifica al cliente por Telegram confirmando la recepción.
5. **Preparación en cocina:** El personal de cocina visualiza la comanda en el Dashboard de Node-RED y, una vez lista, pulsa "Pedido Listo".
6. **Despacho autónomo:** Node-RED traduce la mesa a una pose `{x, y, yaw}` en `map` y envía un goal `NavigateToPose` a Nav2 vía rosbridge.
7. **Llegada y entrega:** Nav2 desplaza el ROSbot 2 PRO hasta la mesa asignada. Se notifica la llegada y se confirma la recogida de los platos.

### Componentes y responsabilidades

| Componente | Responsabilidad | Despliegue previsto |
|---|---|---|
| Bot de Telegram / Web App | Interfaz interactiva de carta, carrito, QR de mesa y avisos | HTML/JS servido por Node-RED (`GET /carta_app`) y túnel Ngrok HTTPS |
| Base de datos (SQLite) | Persistencia local de comandas y estados (`bar.db`, tabla `pedidos`) | Gestionado directamente con nodos SQLite en Node-RED |
| Node-RED | Servidor web de la carta, API de recepción, Dashboard de cocina y orquestador | Servicio en laptop/PC; puerto `1880` |
| Dashboard Cocina | Visualización de comandas pendientes y botón de despacho | Módulo Node-RED Dashboard |
| rosbridge_suite | Puente JSON/WebSocket hacia interfaces ROS 2 | En el grafo ROS 2 Humble del robot, WebSocket normalmente en `9090` |
| Nav2 (`rosbot-autonomy`) | Localización, planificación, navegación a destinos y resultado | Stack de autonomía oficial del ROSbot 2 PRO |
| ROSbot 2 PRO | Base móvil, LiDAR, odometría, IMU y ejecución física | Contenedores del robot |

### Integración propuesta

- Node-RED se ejecutará en un contenedor / servicio local en la laptop/PC, con el puerto `1880` publicado y `/data` persistente para conservar flujos y configuración.
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

Estado: Telegram Mini App, endpoints de comanda en Node-RED (`/carta_app`, `/recibir_pedido`), base de datos SQLite (`bar.db`), túnel Ngrok HTTPS y asignación de mesas por Deep Link QR completados y operativos. Pendientes: Dashboard de cocina, integración rosbridge con Nav2 y pruebas en el mapa.

## 💻 Entorno de desarrollo de Adri

- Laptop inspeccionada el 2026-10-29: Ubuntu 26.04 LTS x86-64, Docker 29.8.2, Docker Compose v5.6.0 y `colcon`; no se encontró ROS 2 nativo (`ros2`) ni `just`.
- ROS 2 Lyrical Luth ya ofrece binarios Tier 1 para Ubuntu 26.04, pero el ROSbot utiliza Humble. Para evitar desalinear herramientas y mensajes del stack actual, empezar con el Compose oficial/subcontenedores y añadir un contenedor de desarrollo Humble si hace falta compilar paquetes propios.
- El Compose PC oficial incluido en `rosbot-autonomy` usa RViz2 Iron y ROS 2 Router; es la ruta prevista por Husarion para la configuración `ros2router` del robot.
- La copia local y la copia del ROSbot están ajustadas a `CONTROLLER=dwb` y `SERIAL_PORT=/dev/ttySERIAL`; `docker compose config --quiet` pasó en ambos equipos. El repositorio remoto del robot está fijado al commit `b4208db70cf88a064ea886256f03e40959c57181`. Las imágenes oficiales se descargaron correctamente.
- Después de la descarga el ROSbot tiene 3,1 GB libres (89 % de uso en `/`). Considerar ese margen antes de desplegar servicios/mapas adicionales; las imágenes antiguas aún ocupan espacio.
- Primer intento controlado de arranque del Compose oficial (2026-10-29): el LiDAR quedó `healthy`, pero el controlador no recibía feedback de IMU por `/dev/ttySERIAL`; el contenedor rosbot quedó `unhealthy` y Nav2 no arrancó. Se detuvo ese intento sin enviar movimiento.
- Se siguió la guía oficial y se ejecutó `just flash-firmware`. La herramienta identificó un STM32F4 (Device ID `0x0413`) y completó escritura y verificación de `firmware-0.11.0.bin` al 100 % por `/dev/ttyS4`. La receta oficial detiene todos los contenedores y usa un contenedor privilegiado para programarlo. [Guía oficial](https://github.com/husarion/rosbot-autonomy/tree/ros2router)
- Compose oficial en marcha tras el flasheo: `rosbot`, `rplidar` y `navigation` `healthy`; `ros2router` activo. Logs confirman hardware controllers de ruedas/IMU y nodos lifecycle de Nav2 activos. La lista de tópicos incluye `/rosbot2r/scan`, `/rosbot2r/odometry/filtered`, `/rosbot2r/imu_broadcaster/imu`, `/rosbot2r/cmd_vel` y tópicos Nav2/SLAM. Las consultas puntuales a `topic info` y `action list` desde varios contenedores no fueron consistentes; resolver descubrimiento DDS y verificar `NavigateToPose` antes de integrar Node-RED.
- El stack anterior (`rosbot`, `microros`, `rplidar` sin prefijo Compose) quedó detenido por la receta de flasheo. No volver a iniciarlo a la vez que el oficial: compartirían el UART `/dev/ttySERIAL` y el puerto del LiDAR.
- No se envió comando de velocidad ni objetivo Nav2. Antes de navegación autónoma hay que crear/cargar el mapa, establecer pose inicial y hacer una prueba física supervisada. Espacio libre: 3,1 GB (89 % usado).

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
- [ROS 2 Lyrical Luth: soporta Ubuntu 26.04 (referencia oficial)](https://github.com/ros2/ros2/releases)
- [Nav2 — Navigation Stack 2](https://docs.nav2.org/)
- [Conceptos de acciones en ROS 2 y NavigateToPose — Nav2](https://docs.nav2.org/jazzy/getting_started/navigation_concepts/ros2.html)
- [rosbridge_suite — protocolo ROS 2 (acciones, topics y servicios)](https://github.com/RobotWebTools/rosbridge_suite/blob/ros2/ROSBRIDGE_PROTOCOL.md)
- [Node-RED en Docker (puerto y persistencia `/data`)](https://nodered.org/docs/getting-started/docker)
- [Node-RED](https://nodered.org/docs/)
- [Nodo de Telegram para Bot API en Node-RED](https://flows.nodered.org/node/node-red-contrib-telegrambot)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Ngrok Docs](https://ngrok.com/docs/)

## 📝 Memoria del Proyecto

- [Memoria LaTeX (Overleaf)](https://www.overleaf.com/project/6ad0f3f618a8107fa81a76ec/share#dd594ebbde5234fac3de13eb5a6ef8c0eabac783d2ebbf31)
