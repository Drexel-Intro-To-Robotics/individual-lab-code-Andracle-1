#!/usr/bin/env python3
import sys
import rospy
import moveit_commander
import geometry_msgs.msg
import copy

class TrajectoryExecutor(object):
    def __init__(self):
        # Initialize the moveit_commander and the rospy node
        moveit_commander.roscpp_initialize(sys.argv)
        rospy.init_node('task8_trajectory_executor', anonymous=True)
        
        # Instantiate a RobotCommander and PlanningSceneInterface
        self.robot = moveit_commander.RobotCommander()
        self.scene = moveit_commander.PlanningSceneInterface()
        
        # The OpenManipulator-X default move group is typically named "arm"
        group_name = "arm"
        self.move_group = moveit_commander.MoveGroupCommander(group_name)

    def execute_joint_space_goal(self, joint_goal):
        """Accepts and executes a joint-space goal."""
        rospy.loginfo("Executing Joint-Space Goal...")
        # The go command can take a list of joint angles
        self.move_group.go(joint_goal, wait=True)
        self.move_group.stop()

    def execute_task_space_goal(self, pose_goal):
        """Accepts and executes a task-space (Cartesian) pose goal."""
        rospy.loginfo("Executing Task-Space Goal...")
        self.move_group.set_pose_target(pose_goal)
        self.move_group.go(wait=True)
        self.move_group.stop()
        self.move_group.clear_pose_targets()

    def execute_waypoints(self, waypoints):
        """Accepts a list of geometry_msgs.msg.Pose waypoints and executes them."""
        rospy.loginfo("Executing Waypoint Trajectory...")
        # compute_cartesian_path interpolates between the provided waypoints
        # eef_step = 0.01 (1 cm resolution), jump_threshold = 0.0 (disabled)
        (plan, fraction) = self.move_group.compute_cartesian_path(waypoints, 0.01, 0.0)
        
        if fraction == 1.0:
            self.move_group.execute(plan, wait=True)
        else:
            rospy.logwarn(f"Only {fraction * 100:.2f}% of the waypoint path was planned.")

if __name__ == '__main__':
    try:
        executor = TrajectoryExecutor()
        # Example usage (uncomment and modify to test):
        
        # 1. Joint Space
        # executor.execute_joint_space_goal([0.0, -1.0, 0.3, 0.7]) 
        
        # 2. Task Space
        # target_pose = geometry_msgs.msg.Pose()
        # target_pose.position.x = 0.2
        # target_pose.position.y = 0.0
        # target_pose.position.z = 0.2
        # target_pose.orientation.w = 1.0
        # executor.execute_task_space_goal(target_pose)

        # ---------------------------------------------------------
        # 3. Testing Waypoints (NEW)
        # ---------------------------------------------------------
        waypoints = []
        
        # Start with the robot's current pose
        wpose = executor.move_group.get_current_pose().pose
        
        # First waypoint: Move UP by 5 cm (0.05 meters)
        wpose.position.z += 0.05
        waypoints.append(copy.deepcopy(wpose))
        
        # Second waypoint: Move RIGHT by 5 cm
        wpose.position.y += 0.05
        waypoints.append(copy.deepcopy(wpose))
        
        # Third waypoint: Move DOWN by 5 cm
        wpose.position.z -= 0.05
        waypoints.append(copy.deepcopy(wpose))
        
        # Execute the generated list
        executor.execute_waypoints(waypoints)
        
    except rospy.ROSInterruptException:
        pass
