# 🖥️ Simulación del robot camarero

Gazebo (Ignition Fortress) con un restaurante sencillo, el **mismo** Nav2/SLAM y los **mismos**
parámetros que el ROSbot real (`../config/nav2_dwb_params.yaml`), RViz2 y el nodo `camarero`.
Así lo que se ajuste aquí se prueba después en el robot con `../deploy.sh`.

## Requisitos

- Docker + Docker Compose y sesión gráfica (X11 o Wayland con XWayland).
- GPU Intel/AMD (`/dev/dri`). Si Gazebo o RViz fallan al dibujar, descomentar
  `LIBGL_ALWAYS_SOFTWARE=1` en `.env` (más lento).
- ~2,2 GB de descarga la primera vez (`./sim.sh pull`); mejor con Wi-Fi, no con datos móviles.
- Unos 4 GB de RAM libres para Gazebo + Nav2 + RViz.

## Uso

```bash
cd rosbot/sim
./sim.sh pull         # solo la primera vez
./sim.sh              # arranca Gazebo + Nav2/SLAM + RViz2 + camarero (Ctrl+C para parar)

# en otra terminal:
./sim.sh pedido 3     # el robot va a mesa_3
./sim.sh estado       # {"estado": "EN_MESA", ...}
./sim.sh entregado    # confirma la recogida -> vuelve a cocina
./sim.sh cancelar     # para y vacía la cola
./sim.sh ros2 topic list
./sim.sh down
```

También se puede mandar el robot a cualquier punto con **Nav2 Goal** en RViz.

## El restaurante (`worlds/`)

```
 y
 3.5 ┌──────────┬───────────────────────────────┐
     │          │      [mesa_1]       [mesa_3]  │
 1.0 │ ▓        │                               │
     │ ▓  R →   puerta                          │   R = robot / cocina (0, 0)
-1.0 │ ▓        │                               │   ▓ = barra de cocina
     │          │      [mesa_2]       [mesa_4]  │
-3.5 └──────────┴───────────────────────────────┘
   -1.5        1.0      3.5            6.5     8.5  x
```

- Para cambiarlo: editar `worlds/generar_restaurante.py` y ejecutar `python3 generar_restaurante.py`.
- Si se mueven mesas, actualizar `../camarero/config/mesas_sim.yaml` (el punto donde se para el robot
  delante de cada mesa).
- Con `SLAM=True` el mapa nace en la posición inicial del robot, que coincide con la cocina (0, 0),
  así que las coordenadas del mundo y del mapa son las mismas.

## Mapa

Con SLAM activo, el mapa se guarda cada 15 s en `maps/` (ignorado por git). Para navegar sobre un mapa
fijo con AMCL: poner `SLAM=False` en `.env` y reiniciar.

## Aislamiento

La simulación usa su propia red de Docker y `ROS_DOMAIN_ID=42`, así que no se mezcla con el ROSbot real
aunque estén en la misma Wi-Fi y usen el mismo namespace `rosbot2r`.
