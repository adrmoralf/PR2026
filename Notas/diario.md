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

### 📝 Observaciones
- La guía actual de Husarion para ROSbot 2R / 2 PRO se mantiene como referencia de puesta en marcha.
- La rama `ros2router` del repositorio oficial separa los contenedores de ROSbot y PC; su receta `just sync` permite sincronizar cambios al robot sin hacer `git pull` por cada edición.
- El protocolo rosbridge para ROS 2 describe publicación/suscripción, servicios y acciones; hay que confirmar que la versión de servidor instalada en Humble soporta las operaciones de acción que necesitará Nav2.
- Confirmar la configuración concreta de sensores y firmware de la unidad antes de cerrar el diseño de la bandeja.
- La conexión al hotspot del móvil tuvo 0 % de pérdida en 20 pings, pero RTT medio 112,7 ms y máximo 331,1 ms; para movimiento autónomo en salón, validar red estable y teleoperación segura.

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

