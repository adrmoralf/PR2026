#!/usr/bin/env bash
# Autora: Irene González
# Instala los paquetes del sistema necesarios para la simulación (requiere sudo).
# Uso: bash instalar_dependencias.sh
set -e

sudo apt-get update
sudo apt-get install -y \
  ros-humble-ign-ros2-control \
  ros-humble-controller-manager \
  ros-humble-controller-interface \
  ros-humble-hardware-interface \
  ros-humble-diff-drive-controller \
  ros-humble-imu-sensor-broadcaster \
  ros-humble-joint-state-broadcaster \
  ros-humble-joint-state-publisher \
  ros-humble-position-controllers \
  ros-humble-ros2controlcli \
  ros-humble-realtime-tools \
  ros-humble-robot-localization \
  ros-humble-laser-filters \
  ros-humble-nav2-common \
  ros-humble-launch-pytest \
  ros-humble-tf-transformations \
  ros-humble-navigation2 \
  ros-humble-nav2-bringup \
  ros-humble-slam-toolbox \
  python3-pyudev python3-serial python3-sh

echo "Dependencias instaladas correctamente."
