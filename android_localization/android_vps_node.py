import rclpy
import os
from android_localization.Events import RecieveEvent
from android_localization.socket_class import SympleServer
from rclpy.node import Node
from sensor_msgs.msg import NavSatFix
from sensor_msgs.msg import Imu
from tf_transformations import quaternion_from_euler
import time
class AndroidVPSNode(Node,metaclass = RecieveEvent):
    def __init__(self):
        super().__init__('android_vps_node')
        #declare timer and publish rate
        self.time=time.time()
        self.rate=0.05#set publish interval
        #create puvlishers
        self.gps_publisher = self.create_publisher(NavSatFix,'gps/fix',1)
        self.imu_publisher = self.create_publisher(Imu,'imu/data',1)
        #get ip address from enviroment value.
        host = os.environ['HOST_IP']
        port = 6000
        #create port with touple
        self.server = SympleServer(str(host),port)
        #register self to listener
        self.server.socket_listener = self

    def onRecieved(self,message):
        gps_msg = NavSatFix()
        imu_msg= Imu()
        try:
            geo_poses=message.split('\n')
            if len(geo_poses[-2])>60:
                print(geo_poses[-2])
                msg_list=geo_poses[-2].split(':')
                msg_data=msg_list[1].split(',')
                #configure gps
                gps_msg.header.frame_id='android_camera'
                gps_msg.header.stamp = self.get_clock().now().to_msg()
                gps_msg.latitude=float(msg_data[0])
                gps_msg.longitude=float(msg_data[1])
                gps_msg.status.service=1
                gps_msg.position_covariance[0]=0.001
                gps_msg.position_covariance[4]=0.001
                gps_msg.position_covariance[8]=0.001

                #configure imu
                x,y,z,w=quaternion_from_euler(0,0,float(msg_data[2]),'ryxz')
                imu_msg.header.stamp = self.get_clock().now().to_msg()
                imu_msg.header.frame_id = 'android_camera'
                imu_msg.orientation.x=x
                imu_msg.orientation.y=y
                imu_msg.orientation.z=z
                imu_msg.orientation.w=w
                if time.time()-self.time>self.rate:
                    self.gps_publisher.publish(gps_msg)
                    self.imu_publisher.publish(imu_msg)
                    print(message)
                    self.time=time.time()

        except:
            print('Imu_gps msg is broken')



    def start(self):
        self.server.accept()

def main():
    print('android_vps_node start')
    rclpy.init()
    node = AndroidVPSNode()
    try:
        node.start()
    except KeyboardInterrupt:
        print('key interrupted')
    
    rclpy.shutdown()
    print('program end')