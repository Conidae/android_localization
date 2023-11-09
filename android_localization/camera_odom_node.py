import rclpy
from rclpy.node import Node

from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseStamped
from tf_transformations import euler_from_quaternion

class CameraOdomNode(Node):
    
    def __init__(self):
        super().__init__('camera_odom_node')
        self.odom_publisher = self.create_publisher(Odometry,'android/odom',1)
        self.pose_sub = self.create_subscription(PoseStamped,'arcore/pose',self.pose_listener,1)
        self.pose_old = PoseStamped()
        self.pose_old.header.stamp = self.get_clock().now().to_msg()
        
    def pose_listener(self,newPose:PoseStamped):
        #calculate dt
        dt = (newPose.header.stamp.nanosec-self.pose_old.header.stamp.nanosec)
        if dt < 0:
            dt+= 10**9
        dt = dt/10**9
        if dt == 0:
            return
        #get previous and new orientations as euler format.
        oldEuler = euler_from_quaternion([
            self.pose_old.pose.orientation.x,
            self.pose_old.pose.orientation.y,
            self.pose_old.pose.orientation.z,
            self.pose_old.pose.orientation.w])
        
        newEuler = euler_from_quaternion([
            newPose.pose.orientation.x,
            newPose.pose.orientation.y,
            newPose.pose.orientation.z,
            newPose.pose.orientation.w])
        
        odom = Odometry()
        odom.header.stamp = newPose.header.stamp
        odom.header.frame_id = 'odom'
        odom.child_frame_id = 'base_footprint'
        odom.pose.pose.position.x = newPose.pose.position.x
        odom.pose.pose.position.y = newPose.pose.position.y
        odom.pose.pose.position.z = newPose.pose.position.z
        
        odom.pose.pose.orientation.x = newPose.pose.orientation.x
        odom.pose.pose.orientation.y = newPose.pose.orientation.y
        odom.pose.pose.orientation.z = newPose.pose.orientation.z
        odom.pose.pose.orientation.w = newPose.pose.orientation.w
        
        odom.pose.covariance = [0.020952,0.0,0.0,0.0,0.0,0.0,
                                0.0,0.009715,0.0,0.0,0.0,0.0,
                                0.0,0.0,0.055828,0.0,0.0,0.0,
                                0.0,0.0,0.0,0.024641,0.0,0.0,
                                0.0,0.0,0.0,0.0,0.031272,0.0,
                                0.0,0.0,0.0,0.0,0.0,0.011522]
        odom.twist.twist.linear.x = (newPose.pose.position.x-self.pose_old.pose.position.x)/dt
        odom.twist.twist.linear.y = (newPose.pose.position.y-self.pose_old.pose.position.y)/dt
        odom.twist.twist.linear.z = (newPose.pose.position.z-self.pose_old.pose.position.z)/dt
        odom.twist.twist.angular.x = (newEuler[0]-oldEuler[0])/dt
        odom.twist.twist.angular.y = (newEuler[1]-oldEuler[1])/dt
        odom.twist.twist.angular.z = (newEuler[2]-oldEuler[2])/dt
        
        odom.twist.covariance = [0.020952,0.0,0.0,0.0,0.0,0.0,
                                0.0,0.009715,0.0,0.0,0.0,0.0,
                                0.0,0.0,0.055828,0.0,0.0,0.0,
                                0.0,0.0,0.0,0.024641,0.0,0.0,
                                0.0,0.0,0.0,0.0,0.031272,0.0,
                                0.0,0.0,0.0,0.0,0.0,0.011522]
        
        self.pose_old = newPose
        
        self.odom_publisher.publish(odom)
        
def main():
    print('odom node start')
    rclpy.init()
    node = CameraOdomNode()
    rclpy.spin(node)
    
        