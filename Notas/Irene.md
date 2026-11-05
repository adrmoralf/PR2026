# 🧑‍💻 Irene — Notas personales

## 🎯 Tarea principal

**Simulación del ROSbot 2 PRO en Gazebo con la distribución ROS 2 acordada para el proyecto**

## 📋 Subtareas

- [ ] **Instalar el entorno de simulación**
  - [ ] Instalar Gazebo compatible con la distribución ROS 2 acordada
  - [ ] Instalar los paquetes de simulación del ROSbot 2 PRO de Husarion
  - [ ] Verificar que el modelo URDF/SDF del robot carga correctamente en Gazebo

- [ ] **Crear el mundo del restaurante**
  - [ ] Diseñar un mapa sencillo del restaurante en Gazebo (paredes, mesas, cocina)
  - [ ] Definir las posiciones de las mesas como waypoints con coordenadas (x, y)
  - [ ] Definir la posición de la cocina (punto de origen del robot)
  - [ ] Guardar el fichero `.world` / `.sdf` en el repositorio

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

_(Apunta aquí lo que vayas descubriendo, problemas, soluciones, etc.)_
