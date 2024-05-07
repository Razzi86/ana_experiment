import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    package_name = 'ana'
    pkg_share = get_package_share_directory(package_name)
    urdf_file_path = os.path.join(pkg_share, 'description', 'robot.urdf.xacro')

    # Convert XACRO to URDF and store it in a temporary file
    urdf_output_path = '/tmp/robot.urdf'
    generate_urdf_command = f"xacro {urdf_file_path} > {urdf_output_path}"

    # Launch Gazebo with the ROS-Ignition bridge
    gz_sim_launch_file_dir = FindPackageShare('ros_ign_gazebo').find('ros_ign_gazebo')
    gz_sim_launch_file = os.path.join(gz_sim_launch_file_dir, 'launch', 'ign_gazebo.launch.py')
    world_file_path = os.path.join(pkg_share, 'worlds', 'default_world.sdf')

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(gz_sim_launch_file),
        launch_arguments={'ign_args': f"{world_file_path} -r"}.items()
    )

    # Node to spawn the robot in Gazebo after URDF is generated
    spawn_entity = Node(
        package='ros_ign_gazebo',
        executable='create',
        arguments=[
            '-file', urdf_output_path,
            '-name', 'ana_robot',
            '-x', '0',
            '-y', '0',
            '-z', '0'
        ],
        output='screen'
    )

    # Start RViz
    rviz_config_path = os.path.join(pkg_share, 'config', 'ana.rviz')
    rviz2 = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config_path],
        output='screen'
    )

    return LaunchDescription([
        ExecuteProcess(
            cmd=['bash', '-c', generate_urdf_command],
            output='screen'
        ),
        gazebo,
        spawn_entity,
        rviz2
    ])

