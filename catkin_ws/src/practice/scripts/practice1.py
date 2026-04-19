#!/usr/bin/env python3
import rospy

def main():
    # Initialize the node with a name
    rospy.init_node('practice_node')
    
    # Set a loop rate of 1 Hz (1 time per second)
    rate = rospy.Rate(1) 
    
    while not rospy.is_shutdown():
        rospy.loginfo("Hello from practice1.py!")
        rate.sleep()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass