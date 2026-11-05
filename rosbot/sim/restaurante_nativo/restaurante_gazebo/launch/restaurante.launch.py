# Autora: Irene González
"""Lanza el restaurante en Gazebo Fortress con el ROSbot 2 PRO en la cocina.

Ejemplos:
    ros2 launch restaurante_gazebo restaurante.launch.py
    ros2 launch restaurante_gazebo restaurante.launch.py escenario:=personas
    ros2 launch restaurante_gazebo restaurante.launch.py escenario:=hora_punta headless:=True rviz:=False

Escenarios (config/escenarios.yaml): vacio, obstaculos, mesa_bloqueada, personas, hora_punta.
"""

import os

import yaml
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    LogInfo,
    OpaqueFunction,
    SetEnvironmentVariable,
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node, SetParameter, SetRemap

PKG = "restaurante_gazebo"


def lanzar(context):
    share = get_package_share_directory(PKG)
    escenario = LaunchConfiguration("escenario").perform(context)
    # Se leen YA: en Humble, los argumentos que se pasan a un include sobrescriben los nuestros
    # para el resto del launch (ERR-009).
    abrir_rviz = LaunchConfiguration("rviz").perform(context).lower() == "true"
    ns = LaunchConfiguration("namespace").perform(context)
    archivo_escenarios = os.path.join(share, "config", "escenarios.yaml")
    with open(archivo_escenarios, encoding="utf-8") as f:
        escenarios = yaml.safe_load(f)["escenarios"]
    if escenario not in escenarios:
        raise RuntimeError(f"Escenario '{escenario}' no existe. Opciones: {', '.join(escenarios)}")
    esc = escenarios[escenario]
    personas = esc.get("personas") or []

    sin_ventana = LaunchConfiguration("headless").perform(context).lower() == "true"
    software_gl = LaunchConfiguration("software_gl").perform(context).lower() == "true"
    config_robot = os.path.join(share, "robot_config")  # copia de Husarion sin cámara (ERR-004)
    mundo = os.path.join(share, "worlds", f"{escenario}.sdf")

    acciones = [LogInfo(msg=f"[restaurante] Escenario '{escenario}': {esc.get('descripcion', '')}")]

    # Nodos propios primero: los SetRemap de más abajo solo afectan a lo que va después.
    # RViz con nuestra configuración: láser, odometría y mapa en el namespace del robot.
    if abrir_rviz:
        acciones.append(Node(
            package="rviz2",
            executable="rviz2",
            name="rviz2",
            arguments=["-d", os.path.join(share, "config", "restaurante.rviz")],
            parameters=[{"use_sim_time": True}],
            remappings=[("/tf", f"/{ns}/tf"), ("/tf_static", f"/{ns}/tf_static")],
            output="log",
        ))

    if personas:
        puentes = []
        for p in personas:
            n = p["nombre"]
            puentes.append(f"/model/{n}/cmd_vel@geometry_msgs/msg/Twist]ignition.msgs.Twist")
            puentes.append(f"/model/{n}/pose@geometry_msgs/msg/Pose[ignition.msgs.Pose")
        acciones.append(Node(
            package="ros_gz_bridge",
            executable="parameter_bridge",
            name="personas_bridge",
            arguments=puentes,
            parameters=[{"use_sim_time": True}],
            output="screen",
        ))
        acciones.append(Node(
            package=PKG,
            executable="personas_node.py",
            name="personas_node",
            parameters=[{"use_sim_time": True, "escenarios_file": archivo_escenarios, "escenario": escenario}],
            output="screen",
        ))

    # --- Simulación: equivalente a rosbot_gazebo/simulation.launch.py, pero arrancando Gazebo
    # nosotros. Husarion usa "--headless-rendering" sin ventana, que solo funciona con ogre2, y en
    # VirtualBox no funcionaba (ERR-010). Sin ventana usamos "-s" (solo servidor).
    if sin_ventana:
        gz_args = f"-s -r -v 1 {mundo}"
    else:
        gz_args = f"--gui-config {os.path.join(share, 'config', 'gazebo_gui.config')} -r -v 1 {mundo}"

    if software_gl:
        # OpenGL por software (Mesa llvmpipe) solo para Gazebo y los nodos que van detrás de esta acción.
        # Con el driver de VirtualBox, el LiDAR (gpu_lidar) mide mal con ogre2 (todo infinito) y con
        # ogre (todo a distancia mínima). Con llvmpipe mide bien y además va más rápido (ERR-010).
        acciones.append(SetEnvironmentVariable("LIBGL_ALWAYS_SOFTWARE", "1"))

    acciones += [
        SetRemap("/diagnostics", "diagnostics"),
        SetRemap("/tf", "tf"),
        SetRemap("/tf_static", "tf_static"),
        SetParameter(name="use_sim_time", value=True),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(get_package_share_directory("ros_gz_sim"), "launch", "gz_sim.launch.py")
            ),
            launch_arguments={"gz_args": gz_args, "on_exit_shutdown": "true"}.items(),
        ),
        Node(
            package="ros_gz_bridge",
            executable="parameter_bridge",
            name="gz_bridge",
            parameters=[{"config_file": os.path.join(config_robot, "rosbot_gazebo", "config", "gz_bridge.yaml")}],
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(get_package_share_directory("rosbot_gazebo"), "launch", "spawn_robot.launch.py")
            ),
            launch_arguments={
                "config_dir": config_robot,
                "robot_model": "rosbot",  # ROSbot 2R / 2 PRO
                "namespace": ns,
                "x": LaunchConfiguration("x").perform(context),
                "y": LaunchConfiguration("y").perform(context),
                "yaw": LaunchConfiguration("yaw").perform(context),
            }.items(),
        ),
    ]
    return acciones


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument(
            "escenario",
            default_value="vacio",
            description="Escenario de prueba: vacio, obstaculos, mesa_bloqueada, personas, hora_punta.",
        ),
        DeclareLaunchArgument(
            "namespace",
            default_value="rosbot2r",
            description="Namespace del robot (el ROSbot real usa 'rosbot2r').",
        ),
        DeclareLaunchArgument("rviz", default_value="True", description="Abrir RViz2."),
        DeclareLaunchArgument(
            "headless",
            default_value="False",
            choices=["True", "False"],
            description="Gazebo sin ventana (más ligero).",
        ),
        DeclareLaunchArgument(
            "software_gl",
            default_value="True",
            choices=["True", "False"],
            description="OpenGL por software para Gazebo (necesario en VirtualBox; False en un equipo con GPU).",
        ),
        DeclareLaunchArgument("x", default_value="0.0", description="Posición inicial x (cocina)."),
        DeclareLaunchArgument("y", default_value="0.0", description="Posición inicial y (cocina)."),
        DeclareLaunchArgument("yaw", default_value="0.0", description="Orientación inicial."),
        OpaqueFunction(function=lanzar),
    ])
