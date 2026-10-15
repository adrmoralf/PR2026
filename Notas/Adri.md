# 🧑‍💻 Adri — Notas personales

## 🎯 Tarea principal

**Instalación y configuración de ROS2 Humble en los ROSbot 2R**

## 📋 Subtareas

- [ ] **Preparar el entorno de desarrollo en el PC**
  - [ ] Instalar Ubuntu 22.04 (compatible con Humble)
  - [ ] Instalar ROS2 Humble en el PC de desarrollo
  - [ ] Configurar el workspace de ROS2 (`colcon build`, sourcing, etc.)

- [ ] **Puesta en marcha del ROSbot 2R**
  - [ ] Seguir el [Quick Start de Husarion](https://husarion.com/tutorials/howtostart/rosbot2r-quick-start/)
  - [ ] Flashear/actualizar el firmware del ROSbot 2R si es necesario
  - [ ] Verificar que el robot arranca correctamente con ROS2 Humble

- [ ] **Configurar la red entre PC y robot**
  - [ ] Conectar PC y ROSbot a la misma red Wi-Fi
  - [ ] Configurar `ROS_DOMAIN_ID` para evitar conflictos
  - [ ] Verificar comunicación con `ros2 topic list` desde el PC

- [ ] **Probar sensores del robot**
  - [ ] Comprobar datos del LiDAR (RPLIDAR A2) — `ros2 topic echo /scan`
  - [ ] Comprobar la cámara RGB-D (Orbbec Astra)
  - [ ] Comprobar la IMU (BNO055)
  - [ ] Comprobar los encoders de las ruedas (odometría)

- [ ] **Instalar dependencias de navegación**
  - [ ] Instalar Nav2 (`sudo apt install ros-humble-navigation2 ros-humble-nav2-bringup`)
  - [ ] Instalar SLAM Toolbox (`ros-humble-slam-toolbox`)
  - [ ] Verificar que los paquetes del ROSbot 2R están disponibles

- [ ] **Test básico de movimiento**
  - [ ] Teleoperar el robot con `ros2 run teleop_twist_keyboard teleop_twist_keyboard`
  - [ ] Confirmar que el robot se mueve correctamente con `/cmd_vel`

## 📝 Notas

_(Apunta aquí lo que vayas descubriendo, problemas, soluciones, etc.)_

