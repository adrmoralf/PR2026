# 🧑‍💻 Irene — Notas personales

## 🎯 Tarea principal

**Simulación del ROSbot 2 PRO en Gazebo con la distribución ROS 2 acordada para el proyecto**

## 📋 Subtareas

- [ ] **Instalar el entorno de simulación**
  - [ ] Instalar Gazebo compatible con la distribución ROS 2 acordada
  - [ ] Instalar los paquetes de simulación del ROSbot 2 PRO de Husarion
  - [ ] Verificar que el modelo URDF/SDF del robot carga correctamente en Gazebo

- [ ] **Crear el mundo del restaurante**
  - [x] Diseñar un mapa sencillo del restaurante en Gazebo (paredes, mesas, cocina)
  - [x] Definir las posiciones de las mesas como waypoints con coordenadas (x, y)
  - [x] Definir la posición de la cocina (punto de origen del robot)
  - [x] Guardar el fichero `.world` / `.sdf` en el repositorio

- [ ] **SLAM — Mapeo del entorno**
  - [ ] Lanzar SLAM Toolbox en simulación para generar un mapa 2D
  - [ ] Teleoperar el robot virtual para recorrer todo el restaurante
  - [ ] Guardar el mapa generado (`.pgm` + `.yaml`) para usarlo en navegación

- [ ] **Navegación autónoma con Nav2**
  - [ ] Lanzar Nav2 con el mapa generado
  - [ ] Probar la localización con AMCL
  - [ ] Enviar goals de navegación desde RViz2 y verificar que el robot llega
  - [ ] Probar navegación por waypoints (cocina → mesa 1 → cocina → mesa 2...)

- [ ] **Validar el flujo completo en simulación**
  - [ ] Simular un pedido: el robot va de cocina a una mesa y vuelve
  - [ ] Probar con múltiples mesas consecutivas
  - [ ] Verificar que el robot evita obstáculos dinámicos (personas, sillas)

- [ ] **Documentar la simulación**
  - [ ] Anotar los parámetros de Nav2 que funcionen bien
  - [ ] Capturas/vídeos de la simulación funcionando
  - [ ] Crear un launch file que arranque todo (Gazebo + Nav2 + RViz2)

## 📝 Notas

- 2026-11-05 (Adri): hay un entorno de simulación base en [`rosbot/sim/`](../rosbot/sim/README.md): Gazebo Fortress con el ROSbot (`husarion/rosbot-gazebo:humble-0.13.0`), un restaurante sencillo (cocina + 4 mesas, generado con `worlds/generar_restaurante.py`), Nav2/SLAM con los mismos parámetros que el robot real, RViz2 y el nodo `camarero`. Se lanza con `./sim.sh`. Preparado para GPU Intel (sin NVIDIA). **Aún no se ha ejecutado** (faltan ~2,2 GB de imágenes); sirve como punto de partida para las subtareas de mundo, SLAM, Nav2 y waypoints.
- **2026-11-05:** Creado el paquete [`rosbot/sim/restaurante_nativo/restaurante_gazebo`](../rosbot/sim/restaurante_nativo/README.md): mundo SDF generado desde `config/restaurante.yaml` (6 mesas + cocina), catálogo de waypoints `mesa_N → {x, y, yaw}` y launch que reutiliza `rosbot_gazebo` (rama `humble` de `rosbot_ros`) con namespace `rosbot2r`.
- El origen del mundo es la salida del robot en la cocina; si SLAM arranca ahí, `map` = `world` y los waypoints valen tal cual para Nav2.
- La simulación Docker de `rosbot-autonomy` exige GPU NVIDIA → se usa una compilación nativa de Humble.
- `ros_components_description` (que usa `rosbot_ros` 0.13.x) ya no existe en GitHub → se usa la rama `humble` de `rosbot_ros`. Pendiente comprobar que los topics coinciden con el robot real.
- **2026-11-05 (tarde):** Restaurante rediseñado: 4 mesas × 4 sillas + cocina, 5 escenarios de prueba (`vacio`, `obstaculos`, `mesa_bloqueada`, `personas`, `hora_punta`) con obstáculos imprevistos y personas móviles. Se lanza con `escenario:=<nombre>`. Waypoints `mesa_1..4` en [rosbot/sim/restaurante_nativo/README.md](../rosbot/sim/restaurante_nativo/README.md).
- **Importante:** parar siempre con `restaurante_gazebo/scripts/parar_simulacion.sh`; si no, Gazebo queda huérfano y el siguiente arranque falla al cargar controladores.
- Rendimiento en mi VM sin GPU: factor de tiempo real ≈ 0,39 (cámara quitada del modelo y paso de física de 4 ms).
- **2026-11-05 (noche):** La simulación se mueve a [`rosbot/sim/restaurante_nativo/`](../rosbot/sim/restaurante_nativo/README.md), junto a la de Docker de Adri (`rosbot/sim/`), sin tocar sus archivos. Es la versión nativa (sin Docker): pendiente de empaquetarla en Docker para el resto del equipo. LiDAR simulado = RPLIDAR A2M12 (como el robot real); en VirtualBox necesita `software_gl:=True` (por defecto).

_(Apunta aquí lo que vayas descubriendo, problemas, soluciones, etc.)_
