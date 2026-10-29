# 🧑‍💻 Adri — Notas personales

## 🎯 Tarea principal

**Puesta en marcha del ROSbot 2 PRO y comprobación de su versión de ROS 2**

## 📋 Subtareas

- [x] **Identificar el entorno del robot antes de instalar o actualizar nada**
  - [x] Comprobar el modelo de SBC/CPU y sistema: UP Board x86-64, Ubuntu 20.04.6 LTS (Focal)
  - [x] Distinguir ROS 2 del host (Foxy) de los contenedores activos (`rosbot`, `microros`, `rplidar`, Humble)
  - [x] Para los comandos ROS y la navegación actuales, usar el entorno Humble del contenedor; en la shell del host falta `/opt/ros/humble/local_setup.bash`
  - [ ] Acordar distribución de desarrollo para PC/simulación sin cambiar ni actualizar el robot a ciegas
- [ ] **Preparar el entorno de desarrollo en el PC**
  - [x] Inventariar el PC: Ubuntu 26.04 LTS x86-64, Docker 29.8.2 y Docker Compose v5.6.0; `colcon` disponible, `ros2` y `just` no encontrados
  - [x] Revisar compatibilidad: el robot ejecuta Humble; el PC puede usar el Compose oficial (`rviz2` Iron + ROS 2 Router) en vez de instalar ROS nativo sin necesidad
  - [ ] Preparar herramientas y workspace de desarrollo Humble en contenedor, o confirmar que el Compose oficial basta para la primera etapa de mapa/navegación
  - [ ] Crear/compilar el workspace de paquetes propios para integración del camarero

- [ ] **Puesta en marcha del ROSbot 2 PRO**
  - [ ] Seguir el [Quick Start de Husarion para ROSbot 2R / 2 PRO](https://husarion.com/tutorials/howtostart/rosbot2r-quick-start/)
  - [x] Flashear el firmware oficial micro-ROS STM32F4 (`firmware-0.11.0.bin`); la herramienta informó escritura/verificación completadas
  - [x] Verificar que los contenedores arrancan y publican los tópicos de sensores y movimiento comprobados

- [ ] **Configurar la red entre PC y robot**
  - [ ] Conectar PC y ROSbot a la misma red Wi-Fi
  - [ ] Estabilizar la conexión laptop–ROSbot antes de teleoperar: el ping por hotspot dio 0 % de pérdida, pero RTT medio de 112,7 ms y máximo de 331,1 ms
  - [ ] Montar la antena Wi-Fi y repetir `ping -c 20 172.20.10.8`; si persiste el jitter, probar una red Wi-Fi estable o Ethernet
  - [ ] Configurar `ROS_DOMAIN_ID` para evitar conflictos
  - [ ] Verificar comunicación con `ros2 topic list` desde el PC

- [ ] **Probar sensores del robot**
  - [ ] Comprobar datos del LiDAR (RPLIDAR A2) — `ros2 topic echo /scan`
  - [ ] Comprobar la cámara RGB-D (Orbbec Astra)
  - [ ] Comprobar la IMU (BNO055)
  - [ ] Comprobar los encoders de las ruedas (odometría)

- [ ] **Instalar dependencias de navegación**
  - [ ] Instalar Nav2 para la distribución ROS 2 elegida
  - [ ] Instalar SLAM Toolbox para la distribución ROS 2 elegida
  - [ ] Verificar que los paquetes del ROSbot 2 PRO están disponibles

- [ ] **Test básico de movimiento**
  - [ ] Teleoperar el robot con `ros2 run teleop_twist_keyboard teleop_twist_keyboard`
  - [ ] Confirmar que el robot se mueve correctamente con `/cmd_vel`

## 📝 Notas

### Conexión actual al ROSbot 2 PRO

- Conectado a la red compartida (hotspot) del móvil.
- Comando SSH usado desde la laptop: `ssh husarion@172.20.10.8`
- Usuario del robot: `husarion`.
- IP actual verificada de `wlan0`: `172.20.10.8` (confirmada con `ip -br -4 addr`; usar `hostname -I` si cambia la red).
- Conectado al hotspot del iPhone (`iPhone de Adrián`), en 2,4 GHz; señal medida: `-61 dBm`, recepción 57,8 Mbit/s y transmisión 39,0 Mbit/s.
- Sistema detectado: Ubuntu 20.04.6 LTS (Focal), arquitectura `x86_64`, placa UP Board.
- ROS 2 Foxy está instalado en el sistema base. También aparecen contenedores Docker con imágenes ROS 2 Humble (`rosbot`, `microros` y `rplidar`).
- Al abrir la shell aparece `not found: "/opt/ros/humble/local_setup.bash"`; revisar la configuración de inicio de shell antes de corregirla.
- Verificación ROS 2: `docker exec -it rosbot bash -lc 'source /opt/ros/humble/setup.bash && ros2 topic list'` muestra tópicos de batería, botones, odometría, IMU, sensores de distancia y `/scan`.
- Verificación del LiDAR: `/scan` publica en directo a aproximadamente 10,6 Hz.
- Verificación de odometría: `/odometry/filtered` publica en directo a aproximadamente 30 Hz.
- Verificación de IMU: `/imu_broadcaster/imu` publica en directo aproximadamente entre 270 y 300 Hz.
- Control manual: `/cmd_vel` es `geometry_msgs/msg/Twist` y `rosbot_base_controller` está suscrito. El ejecutable `teleop_twist_keyboard` está disponible dentro del contenedor `rosbot`.
- Prueba inicial de teleoperación: el robot respondió y se movió brevemente con `i`; en esa prueba se indicó pulsar la tecla solo un instante y después parar con `k`.
- Ping laptop → ROSbot (`172.20.10.8`): 20/20 respuestas, 0 % de pérdida; RTT mínimo 12 ms, medio 112,7 ms, máximo 331,1 ms, desviación 95,0 ms. Hay jitter alto pese a que no se perdieron paquetes.
- Proyecto de robot camarero: Node-RED recibe pedidos Telegram, valida la mesa y solicita a Nav2 navegar a la pose guardada de esa mesa. Mantener `/cmd_vel` para teleoperación y confirmar entrega separadamente de la llegada.
- Referencia de despliegue de navegación: submódulo oficial [`rosbot-autonomy`](../rosbot-autonomy) en rama `ros2router`; requiere revisar configuración antes de levantarlo en esta unidad.
- En el PC se verificó Ubuntu 26.04 LTS, Docker 29.8.2, Compose v5.6.0 y `colcon`; no están instalados los comandos nativos `ros2` ni `just`. ROS 2 Lyrical tiene binarios para Ubuntu 26.04, pero no es la distribución que usa el robot; priorizar contenedores del proyecto para mantener compatibilidad con Humble.
- La copia local y la copia en `/home/husarion/rosbot-autonomy` están ajustadas a `CONTROLLER=dwb` y `SERIAL_PORT=/dev/ttySERIAL`, tras confirmar CPU y UART. El robot tiene el commit `b4208db70cf88a064ea886256f03e40959c57181`; `docker compose config --quiet` pasó en ambos equipos.
- Comprobación en el ROSbot (2026-10-29): CPU confirmada `Intel Atom x5-Z8350`; seleccionar DWB o RPP en el despliegue oficial, no MPPI.
- Puerto serie de la base: `/dev/ttySERIAL` es un symlink a `/dev/ttyS4`. `docker inspect microros` confirma que el agente actual usa `/dev/ttySERIAL`; el contenedor `rosbot` actual no recibe un dispositivo serial directamente. El Compose local oficial queda configurado con `SERIAL_PORT=/dev/ttySERIAL`.
- Puerto del LiDAR: el CP2102 `/dev/ttyUSB0` aparece como `/dev/ttyRPLIDAR` en el host y lo recibe el contenedor `rplidar`. No usar este adaptador como `SERIAL_PORT` de la controladora.
- Siguen activos los contenedores previos (`rosbot`, `microros`, `rplidar`); `rplidar` figura `unhealthy` porque falla su healthcheck con “Healthcheck file still not found”, aunque sus logs recientes indican estado SLLidar `OK` y 10 Hz. Antes de arrancar el stack oficial hay que planificar el cambio para que dos agentes no abran simultáneamente `/dev/ttySERIAL` ni dos nodos el LiDAR.
- Intento de descarga de imágenes del Compose oficial: primer intento falló por timeout DNS a Docker Hub; el segundo avanzó muy despacio sobre el hotspot y se canceló tras ~4 min (RPLIDAR llegó a ~40/137 MB). Tras cancelarlo, los contenedores antiguos seguían activos y el espacio libre seguía en 6,8 GB; repetir con Wi-Fi/Ethernet estable.
- Tras instalar la antena del ROSbot, se reanudó y completó `docker compose pull`. Imágenes descargadas: `husarion/rosbot:humble-0.13.1-20240201`, `husarion/navigation2:humble-1.1.12-20240123`, `husarion/rplidar:humble-1.0.1-20240104` y `husarnet/ros2router:1.6.3`.
- Tras la primera prueba fallida por ausencia de feedback de IMU, se ejecutó `just flash-firmware` siguiendo la guía oficial. La herramienta reconoció el STM32F4 (Device ID `0x0413`) y confirmó `Firmware flashing completed successfully` con `firmware-0.11.0.bin` (100 % escrito/verificado en `/dev/ttyS4`).
- Después del flasheo se inició el Compose oficial. Estado verificado: `rosbot` healthy, `rplidar` healthy, `navigation` healthy y `ros2router` activo. Los logs indican que los controladores de ruedas, IMU y joint states quedaron configurados/activados, y Nav2 dejó sus nodos lifecycle activos.
- Desde la lista de tópicos aparecen `/rosbot2r/scan`, `/rosbot2r/odometry/filtered`, `/rosbot2r/imu_broadcaster/imu`, `/rosbot2r/cmd_vel` y tópicos de SLAM/Nav2. Las consultas puntuales `topic info` y `action list` no quedaron verificadas de forma consistente entre contenedores; revisar descubrimiento DDS antes de conectar Node-RED. No se mandó ninguna velocidad ni objetivo de navegación. Aún falta mapa/pose inicial y prueba física supervisada. Espacio libre: 3,1 GB (89 % usado).

_(Apunta aquí lo que vayas descubriendo, problemas, soluciones, etc.)_

