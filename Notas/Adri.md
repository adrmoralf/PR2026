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
  - [ ] Elegir una versión de Ubuntu compatible con la distribución ROS 2 elegida
  - [ ] Instalar esa distribución de ROS 2 en el PC o usar contenedores si el sistema no es compatible
  - [ ] Configurar el workspace de ROS2 (`colcon build`, sourcing, etc.)

- [ ] **Puesta en marcha del ROSbot 2 PRO**
  - [ ] Seguir el [Quick Start de Husarion para ROSbot 2R / 2 PRO](https://husarion.com/tutorials/howtostart/rosbot2r-quick-start/)
  - [ ] Flashear/actualizar el firmware del ROSbot 2 PRO si es necesario
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

_(Apunta aquí lo que vayas descubriendo, problemas, soluciones, etc.)_

