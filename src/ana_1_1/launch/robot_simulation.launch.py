from launch import LaunchDescription
from launch.actions import ExecuteProcess, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    pkg_name = 'ana_1_1'
    pkg_share = get_package_share_directory(pkg_name)

    master_xacro_path = os.path.join(pkg_share, 'description', 'robot.urdf.xacro')
    robot_description_command = Command(['xacro ', master_xacro_path])


    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description_command}],
    )

    joint_state_publisher = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        output='screen'
    )

    # Setup Gazebo
    gz_sim_world = ExecuteProcess(
        cmd=['gz', 'sim', os.path.join(pkg_share, 'worlds', 'ana_robot_world.sdf')],
        output='screen',
        shell=True
    )

    rviz2 = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', os.path.join(pkg_share, 'config', 'ana.rviz')],
        output='screen',
        parameters=[{'use_sim_time': True}],
    )

    # Controller (assuming this is correctly setup)
    controller = Node(
        package=pkg_name,
        executable='controller_node',
        name='robot_controller',
        output='screen',
        parameters=[{'use_sim_time': True}],
    )

    return LaunchDescription([
        joint_state_publisher,
        robot_state_publisher,
        gz_sim_world,
        rviz2,
        controller,
    ])

