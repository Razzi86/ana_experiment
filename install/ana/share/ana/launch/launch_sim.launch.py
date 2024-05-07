import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command
from launch_ros.actions import Node, LifecycleNode

def generate_launch_description():
    package_name = 'ana'
    pkg_share = get_package_share_directory(package_name)
    urdf_file_path = os.path.join(pkg_share, 'description', 'robot.urdf.xacro')
    
    # Process URDF file
    robot_description = Command(['xacro ', urdf_file_path])

    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description}]
    )

    # Setup for Gazebo Sim (GZ Sim)
    gz_sim_launch_file_dir = get_package_share_directory('ros_ign_gazebo')
    gz_sim_launch_file = os.path.join(gz_sim_launch_file_dir, 'launch', 'ign_gazebo.launch.py')
    world_file_path = os.path.join(pkg_share, 'worlds', 'default_world.sdf')

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(gz_sim_launch_file),
        launch_arguments={'ign_args': world_file_path + ' -r'}.items()
    )

    controller_manager_node = LifecycleNode(
        package='controller_manager',
        executable='ros2_control_node',
        namespace='',
        name='controller_manager',
        output='screen',
        parameters=[{'use_sim_time': True}]  # Adjust parameters as needed
    )

    # Controller setup remains the same
    diff_drive_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["diff_cont"],
        output='screen'
    )
    
    joint_broad_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_broad"],
        output='screen'
    )

    rviz2 = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', '/home/aidan/ros_ws/src/ana/config/ana.rviz'],  # Direct path to your specific RViz config
        output='screen'
    )
    
    return LaunchDescription([
        controller_manager_node,
        node_robot_state_publisher,
        gazebo,
        diff_drive_spawner,
        joint_broad_spawner,
        rviz2,
    ])
