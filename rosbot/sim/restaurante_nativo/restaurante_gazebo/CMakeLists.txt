# Autora: Irene González
cmake_minimum_required(VERSION 3.8)
project(restaurante_gazebo)

find_package(ament_cmake REQUIRED)

install(DIRECTORY config launch worlds robot_config DESTINATION share/${PROJECT_NAME})
install(PROGRAMS
  scripts/generar_mundo.py
  scripts/personas_node.py
  scripts/verificar_simulacion.sh
  scripts/parar_simulacion.sh
  DESTINATION lib/${PROJECT_NAME})

ament_package()
