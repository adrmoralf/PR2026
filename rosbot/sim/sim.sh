#!/usr/bin/env bash
# Lanza / controla la simulación del camarero.
#   ./sim.sh              arranca todo (Gazebo + Nav2/SLAM + RViz2 + camarero)
#   ./sim.sh pull         descarga las imágenes (~2,2 GB la primera vez)
#   ./sim.sh down         para y borra los contenedores
#   ./sim.sh pedido 3     envía el robot a la mesa 3
#   ./sim.sh entregado    confirma la entrega (vuelve a cocina)
#   ./sim.sh cancelar     para y vacía la cola
#   ./sim.sh estado       muestra el estado del camarero
#   ./sim.sh ros2 ...     cualquier comando ros2 dentro de la simulación
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"
set -a; source .env; set +a
NS="/${ROBOT_NAMESPACE}"

ros() {
  docker compose exec -T navigation bash -c \
    'source /opt/ros/humble/setup.bash; export ROS_HOME=/tmp/rh; "$@"' _ "$@"
}

case "${1:-up}" in
  up)
    xhost +local:docker >/dev/null
    mkdir -p maps
    docker compose up --remove-orphans ;;
  pull) docker compose pull ;;
  down) docker compose down --remove-orphans ;;
  pedido)
    ros ros2 topic pub --once "$NS/camarero/pedido" std_msgs/msg/String "{data: '${2:?Uso: ./sim.sh pedido <mesa>}'}" ;;
  entregado) ros ros2 topic pub --once "$NS/camarero/entregado" std_msgs/msg/Empty '{}' ;;
  cancelar)  ros ros2 topic pub --once "$NS/camarero/cancelar" std_msgs/msg/Empty '{}' ;;
  estado)    ros ros2 topic echo --once --qos-durability transient_local --qos-reliability reliable \
               "$NS/camarero/estado" std_msgs/msg/String ;;
  ros2) shift; ros ros2 "$@" ;;
  *) sed -n 2,10p "$0"; exit 1 ;;
esac
