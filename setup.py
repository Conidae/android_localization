from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'android_localization'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share',package_name,package_name),glob('android_localization/*.py')),
        (os.path.join('share',package_name,'launch'),glob('launch/*.launch.py')),
        (os.path.join('share',package_name,'config'),glob('config/*.yaml'))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='reita',
    maintainer_email='Conidae52@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'android_vps_node = android_localization.android_vps_node:main',
            'android_pose_node = android_localization.android_pose_node:main',
            'camera_odom_node = android_localization.camera_odom_node:main',
            'android_imu_node = android_localization.android_imu_node:main'
        ],
    },
)
