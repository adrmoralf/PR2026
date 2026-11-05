#!/usr/bin/env python3
# Autora: Irene González
"""Dibuja el plano de cada escenario (vista cenital), con mesas, waypoints, obstáculos y rutas de personas.

Uso: python3 scripts/dibujar_plano.py  ->  genera docs/plano_<escenario>.png
"""

import math
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.patches as pat  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import yaml  # noqa: E402

PKG = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from generar_mundo import RADIO_PERSONA, posiciones_sillas  # noqa: E402


def dibujar(cfg, nombre, esc, out):
    s, c, si = cfg["sala"], cfg["cocina"], cfg["sillas"]
    fig, ax = plt.subplots(figsize=(9, 7))

    ax.add_patch(pat.Rectangle((s["x_min"], s["y_min"]), s["x_max"] - s["x_min"], s["y_max"] - s["y_min"],
                               fill=False, lw=3, ec="0.3"))
    gb = c["grosor_barra"]
    for ya, yb in [(s["y_min"], c["hueco_y_min"]), (c["hueco_y_max"], s["y_max"])]:
        ax.add_patch(pat.Rectangle((c["x_barra"] - gb / 2, ya), gb, yb - ya, color="0.35"))
    ax.text((s["x_min"] + c["x_barra"]) / 2, s["y_max"] - 0.35, "COCINA", ha="center", fontsize=11, weight="bold")
    p = cfg["puerta"]
    ax.plot([s["x_max"], s["x_max"]], [p["y_centro"] - p["ancho"] / 2, p["y_centro"] + p["ancho"] / 2],
            color="saddlebrown", lw=6)
    ax.text(s["x_max"] - 0.1, p["y_centro"] + p["ancho"] / 2 + 0.1, "puerta", ha="right", fontsize=9)

    for m in cfg["mesas"]:
        x, y, t = m["x"], m["y"], m["tamano"]
        if m["forma"] == "cuadrada":
            ax.add_patch(pat.Rectangle((x - t / 2, y - t / 2), t, t, color="peru"))
        else:
            ax.add_patch(pat.Circle((x, y), t / 2, color="peru"))
        ls = si["lado"]
        for dx, dy in posiciones_sillas(si.get("por_mesa", 2), si["distancia_a_mesa"]):
            ax.add_patch(pat.Rectangle((x + dx - ls / 2, y + dy - ls / 2), ls, ls, color="sienna", alpha=0.7))
        ax.text(x, y, str(m["id"]), ha="center", va="center", color="white", weight="bold", fontsize=13)

    for o in esc.get("obstaculos") or []:
        lx, ly, _ = o["tamano"]
        r = pat.Rectangle((o["x"] - lx / 2, o["y"] - ly / 2), lx, ly, color="tab:red", alpha=0.85)
        r.set_transform(matplotlib.transforms.Affine2D().rotate_around(o["x"], o["y"], o.get("yaw", 0.0)) + ax.transData)
        ax.add_patch(r)
        ax.text(o["x"], o["y"] - ly / 2 - 0.12, o["nombre"], ha="center", va="top", fontsize=7, color="tab:red")

    for per in esc.get("personas") or []:
        xs, ys = zip(*per["ruta"])
        ax.plot(xs, ys, "--", color="tab:blue", alpha=0.6)
        ax.add_patch(pat.Circle(per["ruta"][0], RADIO_PERSONA, color="tab:blue"))
        ax.text(xs[0], ys[0] + 0.28, f"{per['nombre']} ({per['velocidad']} m/s)", ha="center", fontsize=7,
                color="tab:blue")

    for wn, w in cfg["waypoints"].items():
        ax.plot(w["x"], w["y"], "o", color="tab:green")
        ax.arrow(w["x"], w["y"], 0.3 * math.cos(w["yaw"]), 0.3 * math.sin(w["yaw"]), head_width=0.1,
                 color="tab:green")
        ax.annotate(wn, (w["x"], w["y"]), textcoords="offset points",
                    xytext=(6, -12 if w["y"] >= 0 else 6), fontsize=8, color="tab:green")

    ax.set_aspect("equal")
    ax.set_xlim(s["x_min"] - 0.4, s["x_max"] + 0.4)
    ax.set_ylim(s["y_min"] - 0.4, s["y_max"] + 0.4)
    ax.set_xlabel("x [m]")
    ax.set_ylabel("y [m]")
    ax.grid(alpha=0.3)
    ax.set_title(f"Escenario «{nombre}»\n{esc.get('descripcion', '')}", fontsize=9)
    fig.savefig(out, dpi=100, bbox_inches="tight")
    plt.close(fig)
    print(f"Plano generado: {out}")


def main():
    cfg = yaml.safe_load((PKG / "config" / "restaurante.yaml").read_text(encoding="utf-8"))
    escenarios = yaml.safe_load((PKG / "config" / "escenarios.yaml").read_text(encoding="utf-8"))["escenarios"]
    carpeta = PKG / "docs"
    carpeta.mkdir(exist_ok=True)
    for viejo in carpeta.glob("plano_*.png"):
        viejo.unlink()
    for nombre, esc in escenarios.items():
        dibujar(cfg, nombre, esc, carpeta / f"plano_{nombre}.png")


if __name__ == "__main__":
    main()
