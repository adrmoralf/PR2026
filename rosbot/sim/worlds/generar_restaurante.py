#!/usr/bin/env python3
"""Genera restaurante.sdf. Editar las listas de abajo y ejecutar:  python3 generar_restaurante.py

Origen (0, 0) = punto de la cocina donde aparece el robot, mirando hacia +x.
Si se mueven mesas, actualizar también camarero/config/mesas_sim.yaml.
"""
from pathlib import Path

ALTO_PARED = 1.0
GROSOR = 0.1

# (nombre, x, y, largo_x, ancho_y, alto, color RGB)
PAREDES = [
    ("pared_oeste", -1.5, 0.0, GROSOR, 7.0, ALTO_PARED),
    ("pared_este", 8.5, 0.0, GROSOR, 7.0, ALTO_PARED),
    ("pared_norte", 3.5, 3.5, 10.0, GROSOR, ALTO_PARED),
    ("pared_sur", 3.5, -3.5, 10.0, GROSOR, ALTO_PARED),
    # Tabique cocina/comedor en x=1.0 con puerta de 2 m (y entre -1 y 1)
    ("tabique_norte", 1.0, 2.25, GROSOR, 2.5, ALTO_PARED),
    ("tabique_sur", 1.0, -2.25, GROSOR, 2.5, ALTO_PARED),
]
MUEBLES = [
    ("barra_cocina", -1.15, 0.0, 0.5, 3.0, 0.9, "0.55 0.35 0.2"),
    ("mesa_1", 3.5, 2.0, 0.8, 0.8, 0.75, "0.8 0.6 0.4"),
    ("mesa_2", 3.5, -2.0, 0.8, 0.8, 0.75, "0.8 0.6 0.4"),
    ("mesa_3", 6.5, 2.0, 0.8, 0.8, 0.75, "0.8 0.6 0.4"),
    ("mesa_4", 6.5, -2.0, 0.8, 0.8, 0.75, "0.8 0.6 0.4"),
]


def caja(nombre, x, y, sx, sy, sz, color="0.85 0.85 0.85"):
    geo = f"<geometry><box><size>{sx} {sy} {sz}</size></box></geometry>"
    return f"""
    <model name="{nombre}">
      <static>true</static>
      <pose>{x} {y} {sz / 2} 0 0 0</pose>
      <link name="link">
        <collision name="collision">{geo}</collision>
        <visual name="visual">{geo}
          <material><ambient>{color} 1</ambient><diffuse>{color} 1</diffuse></material>
        </visual>
      </link>
    </model>"""


CABECERA = """<?xml version="1.0" ?>
<!-- GENERADO por generar_restaurante.py: no editar a mano. -->
<sdf version="1.6">
  <world name="restaurante">
    <physics name="1ms" type="ignored">
      <max_step_size>0.001</max_step_size>
      <real_time_factor>1.0</real_time_factor>
    </physics>

    <plugin filename="ignition-gazebo-contact-system" name="gz::sim::systems::Contact" />
    <plugin filename="ignition-gazebo-imu-system" name="gz::sim::systems::Imu" />
    <plugin filename="ignition-gazebo-physics-system" name="gz::sim::systems::Physics" />
    <plugin filename="ignition-gazebo-scene-broadcaster-system" name="gz::sim::systems::SceneBroadcaster" />
    <plugin filename="ignition-gazebo-sensors-system" name="gz::sim::systems::Sensors" />
    <plugin filename="ignition-gazebo-user-commands-system" name="gz::sim::systems::UserCommands" />

    <light type="directional" name="sol">
      <cast_shadows>true</cast_shadows>
      <pose>0 0 10 0 0 0</pose>
      <diffuse>0.8 0.8 0.8 1</diffuse>
      <specular>0.2 0.2 0.2 1</specular>
      <direction>-0.5 0.1 -0.9</direction>
    </light>

    <model name="suelo">
      <static>true</static>
      <link name="link">
        <collision name="collision"><geometry><plane><normal>0 0 1</normal><size>30 30</size></plane></geometry></collision>
        <visual name="visual"><geometry><plane><normal>0 0 1</normal><size>30 30</size></plane></geometry>
          <material><ambient>0.7 0.7 0.7 1</ambient><diffuse>0.7 0.7 0.7 1</diffuse></material>
        </visual>
      </link>
    </model>"""

if __name__ == "__main__":
    cuerpo = "".join(caja(*p) for p in PAREDES) + "".join(caja(*m) for m in MUEBLES)
    salida = Path(__file__).with_name("restaurante.sdf")
    salida.write_text(CABECERA + cuerpo + "\n  </world>\n</sdf>\n", encoding="utf-8")
    print(f"Escrito {salida}")
