#!/usr/bin/env bash
# Autora: Irene González
# Para la simulación del restaurante por completo.
# Motivo: al cerrar el launch, el proceso "ign gazebo" (servidor) puede quedarse vivo en segundo plano.
# Al relanzar, el robot nuevo se conecta a ese servidor viejo y falla la carga de controladores
# ("Controller already loaded" / "Failed to configure controller"). Ver ERR-005.
# Uso: bash parar_simulacion.sh
#
# Los patrones van anclados al principio de la línea de comandos (^...) para que pkill NO mate
# a la terminal que llama a este script si su línea contiene esas palabras (ERR-011).

LAUNCH='^/usr/bin/python3 /opt/ros/humble/bin/ros2 launch restaurante_gazebo'
GAZEBO='^(ruby /usr/bin/)?ign gazebo'
NODOS=(
  '^/opt/ros/humble/lib/ros_gz_bridge/parameter_bridge'
  '^/opt/ros/humble/lib/robot_localization/ekf_node'
  '^/opt/ros/humble/lib/robot_state_publisher/robot_state_publisher'
  '^/opt/ros/humble/lib/laser_filters/scan_to_scan_filter_chain'
  '^/opt/ros/humble/lib/joy/joy_node'
  '^/opt/ros/humble/lib/teleop_twist_joy/teleop_node'
  '^/opt/ros/humble/lib/rviz2/rviz2'
  '^/usr/bin/python3 [^ ]*/personas_node\.py'
)

pkill -INT -f "$LAUNCH" 2>/dev/null
for _ in $(seq 10); do
  pgrep -f "$LAUNCH" >/dev/null || break
  timeout 1 tail -f /dev/null
done

# Servidores de Gazebo huérfanos y nodos que hayan quedado colgados
pkill -TERM -f "$GAZEBO" 2>/dev/null
for patron in "${NODOS[@]}"; do
  pkill -TERM -f "$patron" 2>/dev/null
done
timeout 3 tail -f /dev/null
pkill -KILL -f "$GAZEBO" 2>/dev/null

if pgrep -f "$GAZEBO" >/dev/null; then
  echo "AVISO: sigue habiendo procesos de Gazebo:"; pgrep -af "$GAZEBO"
else
  echo "Simulación parada. No quedan procesos de Gazebo."
fi
