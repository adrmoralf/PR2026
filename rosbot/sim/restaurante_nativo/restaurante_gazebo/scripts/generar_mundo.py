#!/usr/bin/env python3
# Autora: Irene González
"""Genera un mundo de Gazebo Fortress por escenario: worlds/<escenario>.sdf.

Lee config/restaurante.yaml (sala, cocina, mesas, sillas) y config/escenarios.yaml
(obstáculos estáticos y personas móviles de cada escenario).

Uso (desde cualquier carpeta):
    python3 scripts/generar_mundo.py
"""

import math
from pathlib import Path

import yaml

PKG = Path(__file__).resolve().parent.parent

# Colores RGBA
MADERA = "0.55 0.35 0.2 1"
MADERA_OSCURA = "0.35 0.2 0.1 1"
PARED = "0.93 0.9 0.83 1"
BARRA = "0.3 0.3 0.35 1"
ACERO = "0.75 0.75 0.78 1"
PUERTA = "0.45 0.25 0.1 1"
SUELO = "0.7 0.65 0.55 1"
OBSTACULO = "0.85 0.15 0.15 1"   # rojo: objetos que no están en el mapa
PERSONA = "0.15 0.35 0.8 1"      # azul
PIEL = "0.9 0.75 0.6 1"

RADIO_PERSONA = 0.2
ALTO_PERSONA = 1.7


def material(rgba):
    return f"<material><ambient>{rgba}</ambient><diffuse>{rgba}</diffuse></material>"


def caja(nombre, x, y, z, sx, sy, sz, rgba, colision=True, yaw=0.0):
    """Link con una caja centrada en (x, y, z)."""
    geo = f"<geometry><box><size>{sx:.3f} {sy:.3f} {sz:.3f}</size></box></geometry>"
    col = f'<collision name="col">{geo}</collision>' if colision else ""
    return (
        f'<link name="{nombre}"><pose>{x:.3f} {y:.3f} {z:.3f} 0 0 {yaw:.4f}</pose>'
        f'{col}<visual name="vis">{geo}{material(rgba)}</visual></link>'
    )


def cilindro(nombre, x, y, z, r, h, rgba):
    geo = f"<geometry><cylinder><radius>{r:.3f}</radius><length>{h:.3f}</length></cylinder></geometry>"
    return (
        f'<link name="{nombre}"><pose>{x:.3f} {y:.3f} {z:.3f} 0 0 0</pose>'
        f'<collision name="col">{geo}</collision><visual name="vis">{geo}{material(rgba)}</visual></link>'
    )


def modelo(nombre, links):
    return f'<model name="{nombre}"><static>true</static>{"".join(links)}</model>'


def paredes(s):
    g, h = s["grosor_pared"], s["alto_pared"]
    x0, x1, y0, y1 = s["x_min"], s["x_max"], s["y_min"], s["y_max"]
    lx, ly = x1 - x0, y1 - y0
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    return modelo("paredes", [
        caja("norte", cx, y1 + g / 2, h / 2, lx + 2 * g, g, h, PARED),
        caja("sur", cx, y0 - g / 2, h / 2, lx + 2 * g, g, h, PARED),
        caja("oeste", x0 - g / 2, cy, h / 2, g, ly, h, PARED),
        caja("este", x1 + g / 2, cy, h / 2, g, ly, h, PARED),
    ])


def cocina(s, c):
    xb, gb, hb = c["x_barra"], c["grosor_barra"], c["alto_barra"]
    links = []
    # Barra en dos tramos, con hueco central para que pase el robot.
    tramos = [(s["y_min"], c["hueco_y_min"]), (c["hueco_y_max"], s["y_max"])]
    for i, (ya, yb) in enumerate(tramos):
        links.append(caja(f"barra_{i}", xb, (ya + yb) / 2, hb / 2, gb, yb - ya, hb, BARRA))
    # Encimeras contra la pared trasera, a los lados (fuera del paso del robot).
    xe = s["x_min"] + 0.3
    largo = (s["y_max"] - s["y_min"]) / 2 - 1.0
    for nombre, signo in (("encimera_n", 1), ("encimera_s", -1)):
        yc = signo * (1.0 + largo / 2)
        links.append(caja(nombre, xe, yc, 0.45, 0.6, largo, 0.9, ACERO))
    return modelo("cocina", links)


def puerta(s, p):
    # Panel visual pegado a la pared del fondo (sin colisión).
    x = s["x_max"] - 0.01
    return modelo("puerta", [caja("panel", x, p["y_centro"], 1.05, 0.02, p["ancho"], 2.1, PUERTA, colision=False)])


def posiciones_sillas(n, d):
    """Desplazamientos (dx, dy) y orientación del respaldo de cada silla."""
    lados = [(-d, 0.0), (d, 0.0), (0.0, d), (0.0, -d)]
    if n not in (2, 4):
        raise ValueError("sillas.por_mesa debe ser 2 o 4")
    return lados[:n]


def mesa(m, sillas):
    i, x, y, t = m["id"], m["x"], m["y"], m["tamano"]
    alto, grosor = 0.75, 0.04
    links = []
    if m["forma"] == "cuadrada":
        links.append(caja("tablero", x, y, alto - grosor / 2, t, t, grosor, MADERA))
        d = t / 2 - 0.05
        for k, (dx, dy) in enumerate([(d, d), (d, -d), (-d, d), (-d, -d)]):
            links.append(caja(f"pata_{k}", x + dx, y + dy, (alto - grosor) / 2, 0.05, 0.05, alto - grosor, MADERA_OSCURA))
    else:
        links.append(cilindro("tablero", x, y, alto - grosor / 2, t / 2, grosor, MADERA))
        links.append(cilindro("pie", x, y, (alto - grosor) / 2, 0.06, alto - grosor, MADERA_OSCURA))
        links.append(cilindro("base", x, y, 0.015, 0.25, 0.03, MADERA_OSCURA))
    ds, ls, hs = sillas["distancia_a_mesa"], sillas["lado"], sillas["alto_asiento"]
    for k, (dx, dy) in enumerate(posiciones_sillas(sillas.get("por_mesa", 2), ds)):
        links.append(caja(f"silla_{k}", x + dx, y + dy, hs / 2, ls, ls, hs, MADERA_OSCURA))
        # Respaldo en el lado de la silla más alejado de la mesa.
        rx = x + dx + math.copysign(ls / 2 - 0.02, dx) if dx else x
        ry = y + dy + math.copysign(ls / 2 - 0.02, dy) if dy else y
        sx, sy = (0.04, ls) if dx else (ls, 0.04)
        links.append(caja(f"respaldo_{k}", rx, ry, hs + 0.2, sx, sy, 0.4, MADERA_OSCURA))
    return modelo(f"mesa_{i}", links)


def suelo(s):
    lx, ly = s["x_max"] - s["x_min"] + 2, s["y_max"] - s["y_min"] + 2
    cx, cy = (s["x_min"] + s["x_max"]) / 2, (s["y_min"] + s["y_max"]) / 2
    geo = f"<geometry><plane><normal>0 0 1</normal><size>{lx} {ly}</size></plane></geometry>"
    return (
        f'<model name="suelo"><static>true</static><pose>{cx} {cy} 0 0 0 0</pose><link name="link">'
        f'<collision name="col">{geo}</collision><visual name="vis">{geo}{material(SUELO)}</visual>'
        f"</link></model>"
    )


def obstaculo(o):
    lx, ly, lz = o["tamano"]
    return modelo(f"obst_{o['nombre']}", [
        caja("cuerpo", o["x"], o["y"], lz / 2, lx, ly, lz, OBSTACULO, yaw=o.get("yaw", 0.0))
    ])


def persona(p):
    """Cilindro dinámico movido por VelocityControl. La posición se publica con PosePublisher.

    Topics de Gazebo:  /model/<nombre>/cmd_vel (entrada)   /model/<nombre>/pose (salida)
    """
    x, y = p["ruta"][0]
    nombre = p["nombre"]
    h, r = ALTO_PERSONA, RADIO_PERSONA
    cuerpo = f"<geometry><cylinder><radius>{r}</radius><length>{h - 0.25}</length></cylinder></geometry>"
    cabeza = "<geometry><sphere><radius>0.12</radius></sphere></geometry>"
    return f"""<model name="{nombre}">
      <pose>{x:.3f} {y:.3f} {(h - 0.25) / 2 + 0.005:.3f} 0 0 0</pose>
      <link name="cuerpo">
        <inertial>
          <mass>70</mass>
          <!-- Inercias grandes para que no vuelque si choca con algo -->
          <inertia><ixx>500</ixx><iyy>500</iyy><izz>500</izz><ixy>0</ixy><ixz>0</ixz><iyz>0</iyz></inertia>
        </inertial>
        <collision name="col">{cuerpo}
          <surface><friction><ode><mu>0</mu><mu2>0</mu2></ode></friction></surface>
        </collision>
        <visual name="vis">{cuerpo}{material(PERSONA)}</visual>
        <visual name="cabeza"><pose>0 0 {(h - 0.25) / 2 + 0.12} 0 0 0</pose>{cabeza}{material(PIEL)}</visual>
      </link>
      <plugin filename="ignition-gazebo-velocity-control-system" name="ignition::gazebo::systems::VelocityControl"/>
      <plugin filename="ignition-gazebo-pose-publisher-system" name="ignition::gazebo::systems::PosePublisher">
        <publish_link_pose>false</publish_link_pose>
        <publish_model_pose>true</publish_model_pose>
        <publish_nested_model_pose>true</publish_nested_model_pose>
        <use_pose_vector_msg>false</use_pose_vector_msg>
        <update_frequency>20</update_frequency>
      </plugin>
    </model>"""


def generar(cfg, nombre_escenario, esc):
    s, c = cfg["sala"], cfg["cocina"]
    paso = cfg.get("simulacion", {}).get("paso_fisica", 0.001)
    motor = cfg.get("simulacion", {}).get("motor_render", "ogre2")
    modelos = [suelo(s), paredes(s), cocina(s, c), puerta(s, cfg["puerta"])]
    modelos += [mesa(m, cfg["sillas"]) for m in cfg["mesas"]]
    modelos += [obstaculo(o) for o in esc.get("obstaculos") or []]
    modelos += [persona(p) for p in esc.get("personas") or []]
    cuerpo = "\n    ".join(modelos)
    return f"""<?xml version="1.0" ?>
<!-- Autora: Irene González. ARCHIVO GENERADO por scripts/generar_mundo.py: no editar a mano. -->
<!-- Escenario: {nombre_escenario}. {esc.get('descripcion', '')} -->
<sdf version="1.6">
  <world name="restaurante">
    <physics name="paso" type="ignored">
      <max_step_size>{paso}</max_step_size>
      <real_time_factor>1.0</real_time_factor>
    </physics>
    <plugin filename="ignition-gazebo-physics-system" name="gz::sim::systems::Physics"/>
    <plugin filename="ignition-gazebo-user-commands-system" name="gz::sim::systems::UserCommands"/>
    <plugin filename="ignition-gazebo-scene-broadcaster-system" name="gz::sim::systems::SceneBroadcaster"/>
    <plugin filename="ignition-gazebo-sensors-system" name="gz::sim::systems::Sensors">
      <render_engine>{motor}</render_engine>
    </plugin>
    <plugin filename="ignition-gazebo-imu-system" name="gz::sim::systems::Imu"/>
    <plugin filename="ignition-gazebo-contact-system" name="gz::sim::systems::Contact"/>

    <scene>
      <ambient>0.6 0.6 0.6 1</ambient>
      <background>0.8 0.85 0.9 1</background>
    </scene>

    <light type="directional" name="sol">
      <cast_shadows>false</cast_shadows>
      <pose>0 0 10 0 0 0</pose>
      <diffuse>0.8 0.8 0.8 1</diffuse>
      <specular>0.2 0.2 0.2 1</specular>
      <direction>-0.3 0.2 -0.9</direction>
    </light>

    {cuerpo}
  </world>
</sdf>
"""


def main():
    cfg = yaml.safe_load((PKG / "config" / "restaurante.yaml").read_text(encoding="utf-8"))
    escenarios = yaml.safe_load((PKG / "config" / "escenarios.yaml").read_text(encoding="utf-8"))["escenarios"]
    carpeta = PKG / "worlds"
    carpeta.mkdir(exist_ok=True)
    for viejo in carpeta.glob("*.sdf"):
        viejo.unlink()
    for nombre, esc in escenarios.items():
        out = carpeta / f"{nombre}.sdf"
        out.write_text(generar(cfg, nombre, esc), encoding="utf-8")
        print(f"Mundo generado: {out}")


if __name__ == "__main__":
    main()
