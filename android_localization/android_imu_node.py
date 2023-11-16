#seisakutyuu
import rclpy
import os
from android_localization.Events import RecieveEvent
from android_localization.socket_class import SympleServer
from rclpy.node import Node
from sensor_msgs.msg import Imu
from tf_transformations import quaternion_from_euler
import time
class AndroidPoseNode(Node,metaclass = RecieveEvent):
    def __init__(self):
        super().__init__('android_imu_node')
        #declare timer and publish rate
        self.time=time.time()
        self.rate=0.05#set publish interval
        #create puvlishers
        self.android_imu_publisher = self.create_publisher(Imu,'android/imu',1)
        #get ip address from enviroment value.
        host = os.environ['HOST_IP']
        port = 5000
        #create port with touple
        self.server = SympleServer(str(host),port)
        #register self to listener
        self.server.socket_listener = self

    def onRecieved(self,message):
        print(message)
        
        android_imu_msg = Imu()
        
        try:
            msg=message.split('\n')
            print(msg)
            if len(msg[-2])>100:
                print("check length ok")
                print(msg[-2])
                msg_list=msg[-2].split(':')
                print("split : is ok")
                msg_data=msg_list[1].split(',')
                print("split , is ok")
                android_imu_msg.header.stamp = self.get_clock().now().to_msg()
                print("get header")
                android_imu_msg.header.frame_id='android_imu_sensor'
                
                x,y,z,w=quaternion_from_euler(float(msg_data[0]),float(msg_data[1]),float(msg_data[2]),'ryxz')

                android_imu_msg.angular_velocity.x=float(msg_data[3])
                android_imu_msg.angular_velocity.y=float(msg_data[4])
                android_imu_msg.angular_velocity.z=float(msg_data[5])
                android_imu_msg.angular_velocity_covariance[0]=0.01
                android_imu_msg.angular_velocity_covariance[4]=0.01
                android_imu_msg.angular_velocity_covariance[8]=0.01
                

                android_imu_msg.linear_acceleration.x=float(msg_data[6])
                android_imu_msg.linear_acceleration.y=float(msg_data[7])
                android_imu_msg.linear_acceleration.z=float(msg_data[8])
                android_imu_msg.linear_acceleration_covariance[0]=0.01
                android_imu_msg.linear_acceleration_covariance[4]=0.01
                android_imu_msg.linear_acceleration_covariance[8]=0.01
                #configure imu
                android_imu_msg.header.frame_id = 'android_camera'
                android_imu_msg.orientation.x=x
                android_imu_msg.orientation.y=y
                android_imu_msg.orientation.z=z
                android_imu_msg.orientation.w=w
                android_imu_msg.orientation_covariance[0]=0.01
                android_imu_msg.orientation_covariance[4]=0.01
                android_imu_msg.orientation_covariance[8]=0.01


                


                if time.time()-self.time>self.rate:
                 
                 self.android_imu_publisher.publish(android_imu_msg)
                 print(message)
                 self.time=time.time()

        except:
            print('imu_data is broken')



    def start(self):
        self.server.accept()

def main():
    print('android_imu_node start')
    rclpy.init()
    node = AndroidPoseNode()
    try:
        node.start()
    except KeyboardInterrupt:
        print('key interrupted')
    
    rclpy.shutdown()
    print('program end')