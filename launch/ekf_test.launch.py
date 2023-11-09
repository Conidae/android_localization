import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    ekf_config_path=os.path.join(get_package_share_directory('android_localization'),'config','test_ekf.yaml')

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
            package='tf2_ros',
            executable = 'static_transform_publisher',
            output = 'screen',
            arguments = ['0.0','0.0','0.0','0.0','0.0','0.0','map','odom']
        ),
        Node(
            package='robot_localization',
            executable='ekf_node',
            name='ekf_filter_node_test',
            output='screen',
            parameters=[ekf_config_path],
            remappings=[('odometry/filtered', 'odometry/global'),
                        ('/set_pose', '/initialpose')])

    ])