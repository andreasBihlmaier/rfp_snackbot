from ament_index_python.packages import get_package_share_path

from launch import LaunchDescription
from launch_ros.actions import Node

import math


def generate_launch_description():
    rfp_snackbot_package_path = get_package_share_path('rfp_snackbot')
    rviz_config = str(rfp_snackbot_package_path / 'rviz' / 'tf_and_markers.rviz')

    return LaunchDescription([
        Node(
            package='rfp_utils',
            executable='pub_mesh_marker.py',
            arguments=['--frequency', '1.0', '--materials', 'table', 'table',
                       str(rfp_snackbot_package_path / 'models/table/table.glb')]
        ),
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments=['--x', '-0.5', '--y', '0.3', '--z', '0.673',
                       '--roll', '0.0', '--pitch', '0.0', '--yaw', str(math.pi / 2),
                       '--frame-id', 'room',
                       '--child-frame-id', 'table']
        ),

        Node(
            package='rfp_utils',
            executable='pub_mesh_marker.py',
            arguments=['--frequency', '1.0', '--materials', 'robot', 'robot',
                       str(rfp_snackbot_package_path / 'models/snackbot/snackbot_static.glb')]
        ),
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments=['--x', '0.1', '--y', '0.2', '--z', '0.0',
                       '--roll', '0.0', '--pitch', '0.0', '--yaw', str(math.pi / 2),
                       '--frame-id', 'table',
                       '--child-frame-id', 'robot']
        ),

        Node(
            package='rfp_utils',
            executable='pub_mesh_marker.py',
            arguments=['--frequency', '1.0', '--materials', 'chips_can', 'chips_can',
                       str(rfp_snackbot_package_path / 'models/chips_can/chips_can.glb')]
        ),
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments=['--x', '0.22', '--y', '0.15', '--z', '0.0',
                       '--roll', '0.0', '--pitch', '0.0', '--yaw', str(math.pi),
                       '--frame-id', 'table',
                       '--child-frame-id', 'chips_can']
        ),

        Node(
            package='rfp_utils',
            executable='pub_mesh_marker.py',
            arguments=['--frequency', '1.0',
                       '--scale', '0.001',
                       '--colors', '0.9', '0.9', '0.9', '1.0',
                       'plate', 'plate',
                       str(rfp_snackbot_package_path / 'models/plate/plate.stl')]
        ),
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments=['--x', '0.10', '--y', '0.45', '--z', '0.0',
                       '--roll', '0.0', '--pitch', '0.0', '--yaw', '0.0',
                       '--frame-id', 'table',
                       '--child-frame-id', 'plate']
        ),

        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments=['--x', '0.255', '--y', '0.045', '--z', '0.128',
                       '--roll', str(math.pi), '--pitch', '0.0', '--yaw', str(-math.pi / 2),
                       '--frame-id', 'robot',
                       '--child-frame-id', 'gripper']
        ),


        Node(
            package='rviz2',
            executable='rviz2',
            arguments=['-d', rviz_config],
        ),
    ])
