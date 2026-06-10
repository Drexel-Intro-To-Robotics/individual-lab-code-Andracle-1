#!/usr/bin/env python3
import sys
import rospy
import moveit_commander
import geometry_msgs.msg
import moveit_msgs.msg
from trajectory_msgs.msg import JointTrajectoryPoint
import numpy as np

class PolynomialTrajectoryGenerator(object):
    def __init__(self):
        moveit_commander.roscpp_initialize(sys.argv)
        rospy.init_node('task9_10_polynomial_trajectory', anonymous=True)
        self.move_group = moveit_commander.MoveGroupCommander("arm")

    # ==========================================
    # TASK 9: TASK-SPACE POLYNOMIAL TRAJECTORY
    # ==========================================
    def generate_task_space_cubic(self, start_pose, end_pose, tf, num_points=50):
        """Generates task-space waypoints using cubic polynomial interpolation."""
        waypoints = []
        p0 = np.array([start_pose.position.x, start_pose.position.y, start_pose.position.z])
        pf = np.array([end_pose.position.x, end_pose.position.y, end_pose.position.z])

        # Calculate cubic coefficients 
        a0 = p0
        a2 = 3.0 * (pf - p0) / (tf**2)
        a3 = -2.0 * (pf - p0) / (tf**3)

        # Generate points along the curve
        for i in range(num_points + 1):
            t = i * (tf / float(num_points))
            pt = a0 + a2*(t**2) + a3*(t**3)

            pose = geometry_msgs.msg.Pose()
            pose.position.x = pt[0]
            pose.position.y = pt[1]
            pose.position.z = pt[2]
            pose.orientation = start_pose.orientation # Keep orientation constant
            waypoints.append(pose)

        return waypoints

    def execute_task_space_polynomial(self, target_pose, execution_time=5.0):
        rospy.loginfo("Executing Task-Space Cubic Polynomial (Task 9)...")
        start_pose = self.move_group.get_current_pose().pose
        
        waypoints = self.generate_task_space_cubic(start_pose, target_pose, execution_time)
        (plan, fraction) = self.move_group.compute_cartesian_path(waypoints, 0.01, 0.0)
        
        if fraction > 0.95:
            self.move_group.execute(plan, wait=True)
        else:
            rospy.logwarn(f"Failed to plan complete path. Only planned {fraction * 100:.2f}%")

    # ==========================================
    # TASK 10: JOINT-SPACE POLYNOMIAL TRAJECTORY
    # ==========================================
    def execute_joint_space_polynomial(self, target_joints, execution_time=5.0, num_points=50):
        """Generates and executes a cubic polynomial path mathematically in joint space."""
        rospy.loginfo("Executing Joint-Space Cubic Polynomial (Task 10)...")
        
        start_joints = np.array(self.move_group.get_current_joint_values())
        target_joints = np.array(target_joints)

        # Calculate cubic coefficients for joints
        a0 = start_joints
        a2 = 3.0 * (target_joints - start_joints) / (execution_time**2)
        a3 = -2.0 * (target_joints - start_joints) / (execution_time**3)

        # Build the custom MoveIt trajectory message
        robot_traj = moveit_msgs.msg.RobotTrajectory()
        robot_traj.joint_trajectory.joint_names = self.move_group.get_active_joints()

        for i in range(num_points + 1):
            t = i * (execution_time / float(num_points))
            
            # Position: q(t) = a0 + a2*t^2 + a3*t^3
            q_t = a0 + a2*(t**2) + a3*(t**3)
            
            # Velocity: v(t) = 2*a2*t + 3*a3*t^2
            v_t = 2*a2*t + 3*a3*(t**2)

            point = JointTrajectoryPoint()
            point.positions = q_t.tolist()
            point.velocities = v_t.tolist()
            point.time_from_start = rospy.Duration(t)
            
            robot_traj.joint_trajectory.points.append(point)

        # MoveIt's execute command accepts manually constructed RobotTrajectory messages
        self.move_group.execute(robot_traj, wait=True)

if __name__ == '__main__':
    try:
        generator = PolynomialTrajectoryGenerator()
        
        # ---------------------------------------------------------
        # Testing Task 9 (Task Space)
        # ---------------------------------------------------------
        # target_pose = geometry_msgs.msg.Pose()
        # target_pose.position.x = 0.25
        # target_pose.position.y = 0.1
        # target_pose.position.z = 0.2
        # target_pose.orientation.w = 1.0
        # generator.execute_task_space_polynomial(target_pose, execution_time=4.0)

        # ---------------------------------------------------------
        # Testing Task 10 (Joint Space)
        # Note: To reach the *same goal* as Task 9, plug the joint 
        # angles corresponding to the pose above into this list.
        # ---------------------------------------------------------
        # target_joint_angles = [0.0, -0.5, 0.3, 0.2]
        # generator.execute_joint_space_polynomial(target_joint_angles, execution_time=4.0)
        
    except rospy.ROSInterruptException:
        pass
