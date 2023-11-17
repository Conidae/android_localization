import rclpy
import os
from android_localization.Events import RecieveEvent
from android_localization.socket_class import SympleServer
from rclpy.node import Node
from geometry_msgs.msg import PoseWithCovarianceStamped
from tf_transformations import quaternion_from_euler
import time
class AndroidPoseNode(Node,metaclass = RecieveEvent):
    def __init__(self):
        super().__init__('android_pose_node')
        #declare timer and publish rate
        self.time=time.time()
        self.rate=0.1#set publish interval
        #create puvlishers
        self.pose_publisher = self.create_publisher(PoseWithCovarianceStamped,'arcore/pose',1)
        #get ip address from enviroment value.
        host = os.environ['HOST_IP']
        port = 8080
        #create port with touple
        self.server = SympleServer(str(host),port)
        #register self to listener
        self.server.socket_listener = self

    def onRecieved(self,message):
        print(message)
        
        pose_msg = PoseWithCovarianceStamped()
        try:
            msg=message.split('\n')
            print(msg)
            if len(msg[-2])>80:
                print("check length ok")
                print(msg[-2])
                msg_list=msg[-2].split(':')
                print("split : is ok")
                msg_data=msg_list[1].split(',')
                print("split , is ok")
                pose_msg.header.stamp = self.get_clock().now().to_msg()
                print("get header")
                #Change coodinate System arcore to ROS
                #position: arcore(x,y,z) -> ROS(z,y,x)
                #rotation: arcore(x,y,z,w) -> ROS(z,y,x,-w)
                pose_msg.pose.pose.position.x=-float(msg_data[2])#arcore(z)
                pose_msg.pose.pose.position.y = -float(msg_data[0])#arcore(x)
                pose_msg.pose.pose.position.z=float(msg_data[1])#arcore(y)
                #pose_msg.pose.position.x = -float(msg_data[2])#arcore(z)
                #pose_msg.pose.position.y = -float(msg_data[0])#arcore(x)
                #pose_msg.pose.position.z = float(msg_data[1])#arcore(y)
                
                pose_msg.pose.pose.orientation.x = -float(msg_data[5])#arcore(quat z)
                pose_msg.pose.pose.orientation.y = -float(msg_data[3])#arcore(quat x)
                pose_msg.pose.pose.orientation.z = float(msg_data[4])#arcore(quat y)
                pose_msg.pose.pose.orientation.w = float(msg_data[6])#arcore(quat w)

                pose_msg.pose.covariance = [0.001,0.0,0.0,0.0,0.0,0.0,
                                            0.0,0.001,0.0,0.0,0.0,0.0,
                                            0.0,0.0,0.0,001.0,0.0,0.0,
                                            0.0,0.0,0.0,0.001,0.0,0.0,
                                            0.0,0.0,0.0,0.0,0.001,0.0,
                                            0.0,0.0,0.0,0.0,0.0,0.001] #set covariance

                #pose_msg.pose.orientation.x = -float(msg_data[5])#arcore(quat z)
                #pose_msg.pose.orientation.y = -float(msg_data[3])#arcore(quat x)
                #pose_msg.pose.orientation.z = float(msg_data[4])#arcore(quat y)
                #pose_msg.pose.orientation.w = float(msg_data[6])#arcore(quat w)
                pose_msg.header.frame_id = 'android_camera'
                

               # if time.time()-self.time>self.rate:
                self.pose_publisher.publish(pose_msg)
                print(message)
                 #   self.time=time.time()

        except:
            print('arcore_pose is broken')



    def start(self):
        self.server.accept()

def main():
    print('android_vps_node start')
    rclpy.init()
    node = AndroidPoseNode()
    try:
        node.start()
    except KeyboardInterrupt:
        print('key interrupted')
    
    rclpy.shutdown()
    print('program end')