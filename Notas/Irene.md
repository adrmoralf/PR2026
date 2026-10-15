# 🧑‍💻 Irene — Notas personales

## 🎯 Tarea principal

**Simulación del ROSbot 2R en Gazebo con ROS2 Humble**

## 📋 Subtareas

- [ ] **Instalar el entorno de simulación**
  - [ ] Instalar Gazebo (Ignition Fortress o Gazebo Classic según compatibilidad con Humble)
  - [ ] Instalar los paquetes de simulación del ROSbot 2R de Husarion
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

_(Apunta aquí lo que vayas descubriendo, problemas, soluciones, etc.)_
