#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import math

class myTurtle():
    
    
    def __init__(self) -> None:
        """_summary_
        create all the nessary pubs/subs here and all the nessary other things
        """
        
        self.odom = rospy.Subscriber('/odom', Odometry, self.odom_cb)
        self.Twist = rospy.Publisher('/cmd_vel', Twist, queue_size=10)


        self.posx = 0
        self.posy = 0
        
        self.rate = rospy.Rate(10)
        rospy.on_shutdown(self.stop)
 
    
        

    def nav_to_pose(self, goal):
        # type: (PoseStamped) -> None
        """
        This is a callback function. It should extract data from goal, drive in a striaght line to reach the goal and
        then spin to match the goal orientation.
        :param goal: PoseStamped
        :return:
        """
        pass

    def odom_cb(self,msg:Odometry) ->None:
        """_summary_

        Get the odom and update the internal location of the robot
        Args:
            msg (Odometry): _description_
        """
        self.posx = msg.pose.pose.position.x
        self.poxy = msg.pose.pose.position.y

    
    
    def stop(self)->None:
        """_summary_
        
        Stop moving
        """
        rospy.loginfo("Stopping")
        vel_msg = Twist()
        
        vel_msg.linear.x=0
        vel_msg.learn.y=0
        vel_msg.angular.x=0
        vel_msg.angular.y=0

        self.Twist.publish(vel_msg)
        rospy.loginfo("Stopped")
        
        
        
    def drive_straight(self, dist: float, vel: float)->None:
        """_summary_

        Args:
            dist (_type_): _description_
        """
        while not rospy.is_shutdown():
            self.rate.sleep()

        currentx = self.posx
        currenty = self.posy
        distance = 0

        vel_msg = Twist()
        vel_msg.linear.x=vel
        vel_msg.linear.y=0
        
        rospy.loginfo(f"Forward: {dist}")
        while distance < dist:
            self.Twist.publish(vel_msg)
            self.rate.sleep()
            distance = math.sqrt((self.posx - currentx)**2 +(self.posy - currenty)**2)

        rospy.loginfo("Forward Done")
        self.stop()

        
    
    def spin_wheels(self, u1, u2, time):
        """
        Spin the two wheels

        :param u1: wheel 1 speed
        :param u2: wheel 2 speed
        :param time: time to drive
        :return: None
        """
        pass

    def rotate(self, angle):
        """
        Rotate in place
        :param angle: angle to rotate
        :return: None
        """
        pass
    
    def convert_to_euler(self, quat):
        # type: (Quaternion) -> float
        """
        This might be helpful to have
        :param quat: quaternion 
        :return: euler angles
        """
        

def main():
    """_summary_
    create all the node start up here
    """
    rospy.init_node("turtlebot", anonymous = False)
    Turtle = myTurtle()
    Turtle.drive_straight(2, 0.5)
    




if __name__ == '__main__':
    main()