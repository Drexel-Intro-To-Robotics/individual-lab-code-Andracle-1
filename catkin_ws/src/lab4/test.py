#!/usr/bin/env python
import sys
import rospy
import moveit_commander

def move_turtlebot_arm():
    # 1. Initialize moveit_commander and the ROS node
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node('tb3_arm_commander', anonymous=True)

    # 2. Instantiate a MoveGroupCommander object for the "arm"
    arm_group = moveit_commander.MoveGroupCommander("arm")

    # Optional: Set planning parameters
    arm_group.set_max_velocity_scaling_factor(0.5)
    arm_group.set_max_acceleration_scaling_factor(0.5)

    # 3. Define the target joint values (in radians)
    # The OpenManipulator has 4 joints: joint1, joint2, joint3, joint4
    joint_goal = arm_group.get_current_joint_values()
    joint_goal[0] = 0.0   # Base pan
    joint_goal[1] = -1.0  # Shoulder lift
    joint_goal[2] = 0.3   # Elbow flex
    joint_goal[3] = 0.7   # Wrist flex

    # 4. Plan and execute the motion
    rospy.loginfo("Executing arm movement...")
    arm_group.go(joint_goal, wait=True)

    # 5. Call stop() to ensure there is no residual movement
    arm_group.stop()

if __name__ == '__main__':
    try:
        move_turtlebot_arm()
    except rospy.ROSInterruptException:
        pass
