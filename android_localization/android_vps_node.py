import rclpy
import os
from android_localization.socket_class import SympleServer
from rclpy.node import Node
from sensor_msgs.msg import NavSatFix

class AndroidVPSNode(Node,metaclass = SympleServer):
    def __init__(self):
        super().__init__('android_vps_node')
        self.gps_publisher = self.create_publisher(NavSatFix,'gps/fix',1)
        #get ip address from enviroment value.
        host = os.environ['HOST_IP']
        port = 6000
        #create port with touple
        self.server = SympleServer(str(host),port)
        #register self to listener
        self.server.socket_listener = self

    def onRecieved(self,message):
        print(message)

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