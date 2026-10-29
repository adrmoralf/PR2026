# 📅 Diario de Desarrollo

Registro diario del progreso del proyecto **Robot Gato Sushi** 🐱🍣 — ROSbot 2 PRO + Node-RED + Telegram.

---

## 2026-10-22

### ✅ Tareas realizadas
- **Cambio de plataforma:** el robot del proyecto pasa de ROSbot 2R a **ROSbot 2 PRO**.
- Actualizadas las fichas y tareas del equipo para reflejar el nuevo modelo.
- Inspeccionada la unidad: UP Board x86-64, Ubuntu 20.04.6; el host tiene ROS 2 Foxy y los contenedores activos `rosbot`, `microros` y `rplidar` usan ROS 2 Humble.
- Verificados `/scan` (~10,6 Hz), `/odometry/filtered` (~30 Hz), `/imu_broadcaster/imu` (~270–300 Hz) y el suscriptor de `/cmd_vel` en el controlador.
- Documentada la arquitectura del robot camarero: Telegram → Node-RED → rosbridge/WebSocket → Nav2 `NavigateToPose` → ROSbot → confirmación de llegada/entrega.
- Definido Node-RED como contenedor separado y con datos persistentes; la navegación sigue en el stack oficial `rosbot-autonomy` para ROSbot 2R/2 PRO.
- Añadidas etapas de implementación: mapa, catálogo mesa→pose, prueba supervisada, bot con lista de usuarios permitidos, cola persistente e idempotencia.
- **Sistema de recepción y comanda (Manu):**
  - Integración de base de datos **SQLite** en Node-RED (`bar.db`) con tabla `pedidos` (`id`, `mesa`, `comanda`, `estado`).
  - Evolución de la interfaz de usuario en Telegram: tras probar lectura con regex y botones inline (descartados por caché y dificultad para gestionar el carrito), se implementó la arquitectura definitiva con **Telegram Mini Apps (Web Apps)** en HTML/CSS/JS.
  - Implementados los endpoints en Node-RED: Front-end (`GET /carta_app`) con catálogo interactivo, cálculo de totales y carrito; Back-end (`POST /recibir_pedido`) que inserta en SQLite y confirma el pedido en el chat de Telegram.
  - Despliegue de túnel seguro HTTPS con **Ngrok** (`https://unglazed-record-pedigree.ngrok-free.dev`) para cumplir los requerimientos de Telegram Web Apps.
  - Implementación de asignación autónoma de mesas vía **códigos QR** con Deep Links (`/start NUMERO_MESA`) inyectados dinámicamente en la URL de la Mini App (`?mesa=X`).

### 📝 Observaciones
- La guía actual de Husarion para ROSbot 2R / 2 PRO se mantiene como referencia de puesta en marcha.
- La rama `ros2router` del repositorio oficial separa los contenedores de ROSbot y PC; su receta `just sync` permite sincronizar cambios al robot sin hacer `git pull` por cada edición.
- El protocolo rosbridge para ROS 2 describe publicación/suscripción, servicios y acciones; hay que confirmar que la versión de servidor instalada en Humble soporta las operaciones de acción que necesitará Nav2.
- Confirmar la configuración concreta de sensores y firmware de la unidad antes de cerrar el diseño de la bandeja.
- La conexión al hotspot del móvil tuvo 0 % de pérdida en 20 pings, pero RTT medio 112,7 ms y máximo 331,1 ms; para movimiento autónomo en salón, validar red estable y teleoperación segura.
- Resueltos errores durante la integración del bot y Ngrok: conflictos de caché en nodos Telegram y códigos de error `ERR_NGROK_105` y `ERR_NGROK_3200`.
- Próximos pasos en orquestación: creación de Dashboard de cocina/barra para marcar comandas listas y enlace con despacho autónomo del robot vía Nav2/rosbridge.

## 2026-10-29

### ✅ Tareas realizadas
- Revisado el siguiente bloque de tareas de Adri: preparar el PC para trabajar con el ROSbot 2 PRO.
- Inventario del PC: Ubuntu 26.04 LTS x86-64, Docker 29.8.2, Docker Compose v5.6.0 y `colcon`; no se encontraron `ros2` ni `just` instalados en el host.
- Revisado `rosbot-autonomy`: su Compose para PC usa RViz2 Iron y ROS 2 Router; los servicios del robot usan imágenes Humble.
- Documentada la ruta de desarrollo inicial con contenedores para convivir con Ubuntu 26.04 y mantener alineación con el ROSbot Humble.

### 🚧 Pendiente antes de desplegar el stack físico
- CPU confirmada: Intel Atom x5-Z8350; `mppi` no es compatible. Cambiada la copia local `rosbot-autonomy/.env` a DWB.
- Identificado el puerto de la base: `/dev/ttySERIAL` apunta a `/dev/ttyS4`, y el contenedor actual `microros` utiliza `/dev/ttySERIAL`. Añadido `SERIAL_PORT=/dev/ttySERIAL` al `.env` local.
- Validado en laptop y ROSbot sin levantar servicios con `docker compose config --quiet`; el Compose resuelve `nav2_dwb_params.yaml` y mapea `/dev/ttySERIAL` al servicio rosbot.
- Identificado el LiDAR: el CP2102 `/dev/ttyUSB0` está enlazado por udev como `/dev/ttyRPLIDAR` y asignado al contenedor `rplidar`; no es el puerto de la base.
- El healthcheck de `rplidar` falla porque no encuentra su archivo de salud, aunque el log muestra SLLidar `OK` y 10 Hz. Los tres contenedores anteriores siguen activos; evitar abrir el serial de base con dos agentes o lanzar dos nodos LiDAR al cambiar de stack.
- Copiado el submódulo al ROSbot en `/home/husarion/rosbot-autonomy`, fijado al commit `b4208db70cf88a064ea886256f03e40959c57181`; ajustados allí `CONTROLLER=dwb` y `SERIAL_PORT=/dev/ttySERIAL`.
- Descarga oficial intentada con `docker compose pull`: el primer intento dio timeout DNS; en el segundo, el hotspot descargó muy lento (~40/137 MB de la imagen RPLIDAR tras ~4 min), así que se canceló. Después, los tres contenedores antiguos seguían activos y el espacio libre continuaba en 6,8 GB.
- Después de colocar una antena en el ROSbot, se reanudó y completó la descarga de imágenes (`rosbot`, `navigation2`, `rplidar`, `ros2router`). `docker compose config --quiet` pasó en el robot.
- Se hizo un cambio controlado al Compose oficial con `CONTROLLER=dwb`, deteniendo primero el stack anterior para no duplicar acceso al UART y al LiDAR. El servicio oficial del LiDAR quedó saludable; el controlador rosbot no recibió feedback de IMU por `/dev/ttySERIAL`, sus spawners no encontraron `rosbot2r/controller_manager` y el healthcheck terminó en `unhealthy`. Navigation2 no llegó a arrancar.
- No se envió ningún comando de movimiento ni se actualizó firmware. Se hizo `docker compose down` y se reactivaron los contenedores previos (`rosbot`, `microros`, `rplidar`); `/scan`, `/odometry/filtered` e `/imu_broadcaster/imu` volvieron a estar presentes. El LiDAR estaba aún en `health: starting` al verificar, tras 14 segundos.
- La guía oficial dice que el firmware micro-ROS STM32F4 se debe actualizar antes de iniciar autonomía. Se inspeccionó `justfile`: `flash-firmware` detiene todos los contenedores Docker y usa un contenedor privilegiado para programar el microcontrolador. No se ejecutó; es el paso pendiente, tras confirmar el procedimiento/versión adecuada para esta unidad. [Guía oficial](https://github.com/husarion/rosbot-autonomy/tree/ros2router)
- Con autorización de Adri se ejecutó `just flash-firmware`: detectó STM32F4 (Device ID `0x0413`) y terminó con `Firmware flashing completed successfully`; `firmware-0.11.0.bin` llegó al 100 % escrito/verificado por `/dev/ttyS4`.
- Se arrancó de nuevo el Compose oficial DWB. Los servicios `rosbot`, `rplidar` y `navigation` quedaron `healthy`; `ros2router` está activo. Los logs confirman IMU, controlador base y broadcasters activados, y lifecycle manager de Nav2 con sus nodos activos.
- La lista de tópicos ROS 2 incluye `/rosbot2r/scan`, `/rosbot2r/odometry/filtered`, `/rosbot2r/imu_broadcaster/imu`, `/rosbot2r/cmd_vel` y tópicos de Nav2/SLAM. Las consultas puntuales `topic info` y `action list` entre contenedores no se confirmaron de forma consistente; revisar descubrimiento DDS y `NavigateToPose` antes de enlazar Node-RED. No se publicó velocidad ni se envió un goal. Falta mapa/pose inicial y teleoperación supervisada antes de navegar.
- Los contenedores antiguos quedaron detenidos por `flash-firmware`; mantenerlos apagados para evitar conflicto de UART/LiDAR con el stack oficial. Espacio libre: 3,1 GB (89 % usado).

### Fuentes
- [ROS 2 Lyrical Luth — plataformas y releases oficiales](https://github.com/ros2/ros2/releases)
- [`rosbot-autonomy` — Compose y guía oficial](https://github.com/husarion/rosbot-autonomy/tree/ros2router)

---

## 2026-10-15 (tarde)

### ✅ Tareas realizadas
- **Cambio de rumbo del proyecto:** se abandona el iRobot Create 3 y se adopta el concepto de robot gato sushi camarero.
- Nuevo stack tecnológico definido: **ROSbot 2R** + **Node-RED** + **Bot de Telegram**.
- Actualización completa de `Info.md` con la nueva descripción, objetivos, tecnologías y recursos.
- Se incorporan **Rubén** e **Irene** al equipo.
- Corregido link roto de Husarion y añadido enlace a la memoria en Overleaf.
- **Asignación de tareas por integrante:**
  - 🔧 **Adri** → Instalación de ROS2 Humble en los ROSbot 2R
  - 🌐 **Manu** → Configuración de Node-RED + bot de Telegram
  - 🖥️ **Irene** → Simulación del robot en Gazebo con Nav2
  - 🎨 **Rubén** → Diseño e impresión 3D de la estructura porta-platos (estilo gato sushi)

### 📝 Observaciones
- La idea es que el ROSbot 2R haga de camarero autónomo, llevando platos de cocina a mesas.
- Los pedidos se hacen desde Telegram (cada uno con su móvil) y Node-RED orquesta todo.
- Cada integrante tiene su `.md` con las subtareas detalladas.

---

## 2026-10-15 (mañana)

### ✅ Tareas realizadas
- Inicialización del repositorio del proyecto.
- Creación de la estructura de notas: `Adri.md`, `Manu.md`.
- Creación de archivos de seguimiento: `errores.md`, `diario.md`, `Info.md`.

### 📝 Observaciones
- Primera sesión de trabajo. Se establece la organización del repositorio.

---

<!--
## YYYY-MM-DD

### ✅ Tareas realizadas
- ...

### 🚧 En progreso
- ...

### 📝 Observaciones
- ...

### 🔜 Próximos pasos
- ...
-->
