#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist, PoseStamped
from nav_msgs.msg import Odometry
import math
import tf

class myTurtle():
    
    
    def __init__(self) -> None:
        """_summary_
        create all the nessary pubs/subs here and all the nessary other things
        """
        
        self.odom = rospy.Subscriber('/odom', Odometry, self.odom_cb)
        #self.goal = rospy.Subscriber('/goal', PoseStamped, self.nav_to_pose)
        self.Twist = rospy.Publisher('/cmd_vel', Twist, queue_size=10)


        self.posx = 0
        self.posy = 0
        self.orient = 0
        
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
        '''
        goalx = goal.pose.position.x
        goaly = goal.pose.position.y
        raworient = goal.pose.orientation
        goalorient = self.convert_to_euler(raworient)
        '''
        pass

    def odom_cb(self,msg:Odometry) ->None:
        """_summary_

        Get the odom and update the internal location of the robot
        Args:
            msg (Odometry): _description_
        """
        self.posx = msg.pose.pose.position.x
        self.posy = msg.pose.pose.position.y
        raworient = msg.pose.pose.orientation
        self.orient = self.convert_to_euler(raworient)
    
    
    def stop(self)->None:
        """_summary_
        
        Stop moving
        """
        rospy.loginfo("Stopping")
        vel_msg = Twist()
        
        vel_msg.linear.x=0
        vel_msg.linear.y=0
        vel_msg.angular.z=0
        

        self.Twist.publish(vel_msg)
        rospy.loginfo("Stopped")
        
        
        
    def drive_straight(self, dist: float, vel: float)->None:
        """_summary_

        Args:
            dist (_type_): _description_
        """
        rospy.sleep(1)

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

        :param u1: wheel 1 speed (left)
        :param u2: wheel 2 speed (right)
        :param time: time to drive
        :return: None
        """
        rospy.sleep(1)
        T = 0.287

        linv = (u1 + u2)/2
        angv = (u2 - u1) / T

        vel_msg = Twist()
        vel_msg.linear.x = linv
        vel_msg.angular.z = angv

        rospy.loginfo(f"u1 (left): {u1}, u2 (right): {u2}, time: {time}")
        start = rospy.get_time()
        while rospy.get_time() - start < time:
            self.Twist.publish(vel_msg)
            self.rate.sleep()

        rospy.loginfo("Spin Wheel Done")
        self.stop()
        

    def rotate(self, angle):
        """
        Rotate in place
        :param angle: angle to rotate
        :return: None
        """
        rospy.sleep(1)
        lastO = self.orient
        rotation = 0

        vel_msg = Twist()
        if angle > 0:
            vel_msg.angular.z = 0.3
        elif angle < 0:
            vel_msg.angular.z = -0.3
        else:
            vel_msg.angular.z = 0

        rospy.loginfo(f"Rotating: {angle}")
        while abs(rotation) < abs(angle):
            self.Twist.publish(vel_msg)
            self.rate.sleep()

            currentO = self.orient
            delta = currentO - lastO
            delta = math.atan2(math.sin(delta), math.cos(delta))
            rotation = rotation + abs(delta)
            lastO = currentO

        rospy.loginfo("Rotating Done")
        self.stop()
        
    
    def convert_to_euler(self, quat):
        # type: (Quaternion) -> float
        """
        This might be helpful to have
        :param quat: quaternion 
        :return: euler angles
        """
        roll, pitch, yaw = tf.transformations.euler_from_quaternion([quat.x, quat.y, quat.z, quat.w])
        return yaw



def main():
    """_summary_
    create all the node start up here
    """
    rospy.init_node("turtlebot", anonymous = False)
    Turtle = myTurtle()
    rospy.sleep(1)
    Turtle.drive_straight(2, 0.5)
    Turtle.rotate(math.pi)
    Turtle.spin_wheels(2, 1, 10)
    Turtle.spin_wheels(0, 3, 10)
    
    




if __name__ == '__main__':
    main()