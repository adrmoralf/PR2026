#!/usr/bin/env bash
# Autora: Irene González
# Comprueba que la simulación del restaurante publica la misma interfaz que el ROSbot real
# y que el robot se mueve al mandarle /cmd_vel. Ejecutar CON LA SIMULACIÓN YA LANZADA.
# Uso: bash verificar_simulacion.sh [namespace]   (por defecto rosbot2r)
# Deja el informe en verificacion.txt (carpeta actual) y lo muestra por pantalla.

NS="${1:-rosbot2r}"
OUT="verificacion.txt"
exec > >(tee "$OUT") 2>&1

echo "=== Verificación de la simulación ($(date '+%F %T')), namespace /$NS ==="
echo
echo "--- Topics disponibles ---"
ros2 topic list

echo
echo "--- Factor de tiempo real de Gazebo (1.0 = tiempo real) ---"
stats=$(timeout 15 ign topic -e -t /world/restaurante/stats -n 1 2>/dev/null)
printf '%s\n' "$stats" | grep -m1 real_time_factor || echo "  no disponible"

echo
echo "--- Topics que usa el robot real ---"
TOPICS=$(ros2 topic list)
for t in /$NS/cmd_vel /$NS/scan /$NS/odometry/filtered /$NS/imu_broadcaster/imu /$NS/imu/data /clock; do
  if printf '%s\n' "$TOPICS" | grep -qx "$t"; then
    tipo=$(ros2 topic type "$t" | head -1)
    echo "OK    $t  [$tipo]"
  else
    echo "FALTA $t"
  fi
done

echo
echo "--- Frecuencias (5 s cada uno) ---"
for t in /$NS/scan /$NS/odometry/filtered; do
  echo "$t:"
  # Se guarda la salida completa antes de filtrarla: si grep corta la tubería, ros2 se cierra con
  # BrokenPipeError y Ubuntu muestra "System program problem detected" (ERR-008).
  salida=$(timeout 6 ros2 topic hz "$t" 2>/dev/null)
  printf '%s\n' "$salida" | grep -m1 'average rate' || echo "  sin datos"
done

leer_x() {
  local msg
  msg=$(timeout 10 ros2 topic echo --once "/$NS/odometry/filtered" nav_msgs/msg/Odometry 2>/dev/null)
  printf '%s\n' "$msg" | awk '/position:/{getline; print $2; exit}'
}

echo
echo "--- Prueba de movimiento: 0.2 m/s hacia delante durante ~3 s ---"
x0=$(leer_x)
timeout 3 ros2 topic pub -r 10 "/$NS/cmd_vel" geometry_msgs/msg/Twist "{linear: {x: 0.2}}" > /dev/null 2>&1
ros2 topic pub --once "/$NS/cmd_vel" geometry_msgs/msg/Twist "{}" > /dev/null 2>&1
x1=$(leer_x)
echo "x inicial = ${x0:-?}   x final = ${x1:-?}"
if [ -n "$x0" ] && [ -n "$x1" ] && awk -v a="$x0" -v b="$x1" 'BEGIN{exit !(b-a > 0.1)}'; then
  echo "OK    el robot avanza"
else
  echo "FALLO el robot no se ha movido lo esperado"
fi

echo
echo "--- Frames TF estáticos (child_frame_id) ---"
timeout 10 ros2 topic echo --once --qos-durability transient_local "/$NS/tf_static" tf2_msgs/msg/TFMessage 2>/dev/null \
  | grep child_frame_id | sort -u
echo "--- Frames TF dinámicos (child_frame_id) ---"
timeout 10 ros2 topic echo --once "/$NS/tf" tf2_msgs/msg/TFMessage 2>/dev/null | grep child_frame_id | sort -u

echo
echo "=== Fin. Informe guardado en $(pwd)/$OUT ==="
