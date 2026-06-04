#!/usr/bin/env python3
"""
Launch file for SnackBot arm control.

This launch file sets up the complete ros2_control stack for SnackBot including:
- Robot state publisher for URDF and TF transforms
- Controller manager for hardware interface lifecycle
- Joint state broadcaster for publishing joint states
- Joint trajectory controller for position trajectory execution

The launch file accepts command-line arguments for hardware configuration and supports
both real hardware and mock/simulation mode for testing without motors.

Example usage:
    ros2 launch rfp_snackbot snackbot_control.launch.py serial_port:=/dev/ttyACM0
    ros2 launch rfp_snackbot snackbot_control.launch.py use_mock:=true
"""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    """
    Generate launch description for SnackBot control.

    Returns
    -------
    LaunchDescription
        Complete launch configuration with all nodes and parameters

    """
    # Declare arguments
    declared_arguments = []

    declared_arguments.append(
        DeclareLaunchArgument(
            'serial_port',
            default_value='/dev/ttyACM0',
            description='Serial port for STS motor communication'
        )
    )

    declared_arguments.append(
        DeclareLaunchArgument(
            'baud_rate',
            default_value='1000000',
            description='Serial baud rate'
        )
    )

    declared_arguments.append(
        DeclareLaunchArgument(
            'use_mock',
            default_value='false',
            description='Use mock/simulation mode (no hardware required)'
        )
    )

    # Initialize Arguments
    serial_port = LaunchConfiguration('serial_port')
    baud_rate = LaunchConfiguration('baud_rate')
    use_mock = LaunchConfiguration('use_mock')

    # Get URDF via xacro
    robot_description_content = Command(
        [
            PathJoinSubstitution([FindExecutable(name='xacro')]),
            ' ',
            PathJoinSubstitution(
                [FindPackageShare('rfp_snackbot'), 'urdf',
                 'snackbot_simplified_control.urdf.xacro']
            ),
            ' ',
            'serial_port:=', serial_port,
            ' ',
            'baud_rate:=', baud_rate,
            ' ',
            'use_mock:=', use_mock,
        ]
    )
    robot_description = {
        'robot_description': ParameterValue(robot_description_content, value_type=str)
    }

    # Robot state publisher
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='both',
        parameters=[robot_description],
    )

    # Controller configuration
    controller_config = PathJoinSubstitution(
        [
            FindPackageShare('rfp_snackbot'),
            'config',
            'snackbot_controllers.yaml'
        ]
    )

    # Controller manager
    controller_manager_node = Node(
        package='controller_manager',
        executable='ros2_control_node',
        output='both',
        parameters=[robot_description, controller_config],
    )

    # Joint state broadcaster
    joint_state_broadcaster_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_state_broadcaster', '--controller-manager', '/controller_manager'],
    )

    # Arm controller (joint trajectory controller for position mode)
    arm_controller_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['arm_controller', '--controller-manager', '/controller_manager'],
    )

    nodes = [
        robot_state_publisher_node,
        controller_manager_node,
        joint_state_broadcaster_spawner,
        arm_controller_spawner,
    ]

    return LaunchDescription(declared_arguments + nodes)
