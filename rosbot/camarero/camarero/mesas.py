"""Carga y valida el fichero de mesas (sin dependencias de ROS para poder testearlo)."""

import math
from dataclasses import dataclass

import yaml


@dataclass(frozen=True)
class Pose2D:
    x: float
    y: float
    yaw: float  # radianes

    def quaternion(self):
        """Devuelve (x, y, z, w) para una rotación pura en Z."""
        return (0.0, 0.0, math.sin(self.yaw / 2.0), math.cos(self.yaw / 2.0))


def _a_pose(nombre, datos):
    try:
        return Pose2D(float(datos["x"]), float(datos["y"]), float(datos.get("yaw", 0.0)))
    except (TypeError, KeyError, ValueError) as e:
        raise ValueError(f"Posición inválida para '{nombre}': {datos!r}") from e


def cargar_mesas(ruta):
    """Lee el YAML y devuelve (frame_id, base, {nombre: Pose2D}).

    Formato:
        frame_id: map
        base: cocina
        puntos:
          cocina: {x: 0.0, y: 0.0, yaw: 0.0}
          mesa_1: {x: 3.5, y: 1.25, yaw: 1.5708}
    """
    with open(ruta, encoding="utf-8") as f:
        datos = yaml.safe_load(f) or {}

    puntos = datos.get("puntos") or {}
    if not isinstance(puntos, dict):
        raise ValueError("'puntos' debe ser un diccionario nombre -> {x, y, yaw}")

    poses = {str(n): _a_pose(n, p) for n, p in puntos.items()}
    base = str(datos.get("base", "cocina"))
    if base not in poses:
        raise ValueError(f"La base '{base}' no está definida en 'puntos'")

    return str(datos.get("frame_id", "map")), base, poses


def normalizar_destino(texto, poses):
    """Acepta 'mesa_3', 'Mesa 3', '3' o 'cocina' y devuelve el nombre del punto o None."""
    t = str(texto).strip().lower().replace(" ", "_")
    if t in poses:
        return t
    if t.isdigit() and f"mesa_{t}" in poses:
        return f"mesa_{t}"
    return None
