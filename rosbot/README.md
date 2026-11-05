# 🤖 Stack del ROSbot 2 PRO (navegación)

Esta carpeta es lo que ejecuta el ROSbot en `/home/husarion/rosbot-autonomy`.
Se edita aquí, se versiona en este repo y se envía al robot con `./deploy.sh`.

Parte de [`husarion/rosbot-autonomy`](https://github.com/husarion/rosbot-autonomy/tree/ros2router)
(rama `ros2router`, commit `b4208db70cf88a064ea886256f03e40959c57181`, licencia Apache-2.0 en `LICENSE`).
El README original está en [`README.husarion.md`](README.husarion.md).

## Qué fichero cambia qué

| Fichero | Qué controla | Al desplegar se reinicia |
|---|---|---|
| `.env` | Controlador (`CONTROLLER=dwb`/`rpp`; **no `mppi`**, la CPU Atom no puede), `SLAM`, puertos serie, namespace `rosbot2r` | los servicios afectados |
| `config/nav2_dwb_params.yaml` | **Cómo se mueve con DWB**: velocidades y aceleraciones máximas, costmaps, inflado de obstáculos, tolerancia de llegada, AMCL/planner | `navigation` |
| `config/nav2_rpp_params.yaml` | Lo mismo para el controlador Regulated Pure Pursuit | `navigation` |
| `compose.yaml` | Contenedores del robot: `rosbot` (base + EKF), `rplidar`, `navigation` (Nav2 + SLAM Toolbox), `ros2router` | los servicios cambiados |
| `filter.yaml` | Tópicos/acciones que `ros2router` deja salir del robot | `ros2router` |
| `camarero/` | **Código propio**: nodo que recibe pedidos por mesa y manda el robot con Nav2 | `camarero` (si está activo) |
| `camarero/config/mesas_robot.yaml` | Coordenadas de cocina y mesas en el mapa real | `camarero` |
| `compose.pc.yaml` | RViz2 en el PC | — (se ejecuta en el PC) |
| `sim/` | **Simulación del restaurante** para este proyecto ([`sim/README.md`](sim/README.md)) | — (no se copia al robot) |
| `compose.sim.*.yaml` | Simulaciones originales de Husarion (requieren NVIDIA) | — |

Los ficheros `*_webots_params.yaml` y `nav2_mppi_params.yaml` solo sirven para simulación o como referencia.

## Nodo camarero

Interfaz (todo bajo `/rosbot2r/`, tipos `std_msgs`):

| Tópico | Tipo | Uso |
|---|---|---|
| `camarero/pedido` | `String` | `"mesa_3"`, `"3"` o `"cocina"`. Se encola si el robot está ocupado |
| `camarero/entregado` | `Empty` | El cliente recogió el plato → vuelve a cocina |
| `camarero/cancelar` | `Empty` | Cancela la navegación y vacía la cola |
| `camarero/estado` | `String` (JSON, último valor retenido) | `{"estado", "destino", "cola", "detalle"}` |

Estados: `EN_BASE → YENDO_A_MESA → EN_MESA → VOLVIENDO → (ESPERANDO_SALIDA →) …`, más `PARADO` y `ERROR`.
Si nadie confirma en `espera_en_mesa_s` (60 s) vuelve solo a cocina.

En el robot está **desactivado**. Para activarlo, cuando `mesas_robot.yaml` tenga las mesas reales,
añadir `COMPOSE_PROFILES=camarero` a `.env` y ejecutar `./deploy.sh`.

Tests sin ROS: `cd camarero && PYTHONPATH=. python3 -s -m pytest test`.

## Desplegar en el robot

```bash
cd rosbot
./deploy.sh --dry-run    # ver qué cambiaría
./deploy.sh              # copiar y reiniciar lo necesario
./deploy.sh --pull-map   # traer maps/map.{png,yaml} del robot
```

- Requiere SSH por clave a `husarion@172.20.10.8` (`ssh-copy-id`). Si cambia la IP: `ROBOT=husarion@<ip> ./deploy.sh`.
- `maps/` nunca se sobrescribe en el robot (está en `.gitignore`).
- **Reiniciar `navigation` cancela cualquier objetivo en curso.** No desplegar con el robot navegando.

## Comandos ROS 2 en el robot

Los nodos usan solo memoria compartida (`shm-only.xml`). La CLI debe ejecutarse con el usuario `husarion`, nunca como root:

```bash
docker exec --user husarion rosbot-autonomy-navigation-1 bash -lc \
  'source /opt/ros/humble/setup.bash; export ROS_HOME=/tmp/rh; ros2 topic list'
```
