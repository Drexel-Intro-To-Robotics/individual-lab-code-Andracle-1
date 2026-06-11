#!/usr/bin/env python3
import sys
import rospy
import moveit_commander
import geometry_msgs.msg
import copy

class TrajectoryExecutor(object):
    def __init__(self):
        #Initialize moveit_commander and rospy node
        moveit_commander.roscpp_initialize(sys.argv)
        rospy.init_node('task8_trajectory_executor', anonymous=True)
        
        #Instantiate RobotCommander and PlanningSceneInterface
        self.robot = moveit_commander.RobotCommander()
        self.scene = moveit_commander.PlanningSceneInterface()
        
        group_name = "arm"
        self.move_group = moveit_commander.MoveGroupCommander(group_name)

    def execute_joint_space_goal(self, joint_goal):
        #executes joint-space goal.
        rospy.loginfo("Executing Joint-Space Goal...")
        self.move_group.go(joint_goal, wait=True)
        self.move_group.stop()

    def execute_task_space_goal(self, pose_goal):
        #executes task-space pose goal.
        rospy.loginfo("Executing Task-Space Goal...")
        self.move_group.set_pose_target(pose_goal)
        self.move_group.go(wait=True)
        self.move_group.stop()
        self.move_group.clear_pose_targets()

    def execute_waypoints(self, waypoints):
        #Accepts list of geometry_msgs.msg.Pose waypoints and executes
        rospy.loginfo("Executing Waypoint Trajectory...")
        (plan, fraction) = self.move_group.compute_cartesian_path(waypoints, 0.01, 0.0)
        
        if fraction == 1.0:
            self.move_group.execute(plan, wait=True)
        else:
            rospy.logwarn(f"Only {fraction * 100:.2f}% of the waypoint path was planned.")

if __name__ == '__main__':
    try:
        executor = TrajectoryExecutor()
        #Joint Space
        #executor.execute_joint_space_goal([1.8055, 0.4661, -0, -0.4661]) 
        #executor.execute_joint_space_goal([-1.8892, -0.4456, -0, -0.4456]) 
        
        #Task Space
        #target_pose = geometry_msgs.msg.Pose()
        #target_pose.position.x = 0.2
        #target_pose.position.y = 0
        #target_pose.position.z = 0.2
        #target_pose.orientation.w = 1.0
        #executor.execute_task_space_goal(target_pose)

        # Waypoints
        waypoints = []
        # robot's current pose
        wpose = executor.move_group.get_current_pose().pose
        
        # First waypoint: UP by 5 cm 
        wpose.position.z += 0.05
        waypoints.append(copy.deepcopy(wpose))
        # Second waypoint: RIGHT by 5 cm
        wpose.position.y += 0.05
        waypoints.append(copy.deepcopy(wpose))
        # Third waypoint: DOWN by 5 cm
        wpose.position.z -= 0.05
        waypoints.append(copy.deepcopy(wpose))
        # Execute waypoints
        executor.execute_waypoints(waypoints)
        
    except rospy.ROSInterruptException:
        pass
