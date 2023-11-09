import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    ekf_config_path=os.path.join(get_package_share_directory('android_localization'),'config','ekf_setting.yaml')

    return LaunchDescription([
        Node(
            package='android_localization',
            executable='android_vps_node'
        ),
        Node(
            package='android_localization',
            executable='android_pose_node'
        ),
        Node(
            package='android_localization',
            executable='android_imu_node'
        ),
        Node(
            package='robot_localization',
            executable='ekf_node',
            name='ekf_filter_node_map',
            output='screen',
            parameters=[ekf_config_path],
            remappings=[('odometry/filtered', 'odometry/global'),
                        ('/set_pose', '/initialpose')]),
        Node(
            package='robot_localization',
            executable='ekf_node',
            name='ekf_filter_node_odom',
            output='screen',
            parameters=[ekf_config_path],
            remappings=[('odometry/filtered', 'odometry/local'),
                        ('/set_pose', '/initialpose')]),
        Node(
            package='robot_localization',
            executable='navsat_transform_node',
            name='navsat_transform',
            output='screen',
            parameters=[ekf_config_path],
            remappings=[('imu', 'android/imu'),
                        ('gps/fix', 'gps/fix'), 
                        ('gps/filtered', 'gps/filtered'),
                        ('odometry/gps', 'odometry/gps'),
                        ('odometry/filtered', 'odometry/global')])

    ])