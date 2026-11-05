import math
from pathlib import Path

import pytest

from camarero.mesas import Pose2D, cargar_mesas, normalizar_destino

CONFIG = Path(__file__).resolve().parents[1] / "config"


@pytest.mark.parametrize("fichero", ["mesas_sim.yaml", "mesas_robot.yaml"])
def test_configs_validas(fichero):
    frame, base, poses = cargar_mesas(CONFIG / fichero)
    assert frame == "map"
    assert base in poses


def test_normalizar_destino():
    _, _, poses = cargar_mesas(CONFIG / "mesas_sim.yaml")
    assert normalizar_destino("mesa_3", poses) == "mesa_3"
    assert normalizar_destino(" Mesa 3 ", poses) == "mesa_3"
    assert normalizar_destino("3", poses) == "mesa_3"
    assert normalizar_destino("cocina", poses) == "cocina"
    assert normalizar_destino("9", poses) is None


def test_quaternion():
    _, _, z, w = Pose2D(0, 0, math.pi / 2).quaternion()
    assert z == pytest.approx(math.sqrt(0.5)) and w == pytest.approx(math.sqrt(0.5))


def test_base_inexistente(tmp_path):
    f = tmp_path / "m.yaml"
    f.write_text("base: barra\npuntos:\n  cocina: {x: 0, y: 0}\n")
    with pytest.raises(ValueError):
        cargar_mesas(f)
