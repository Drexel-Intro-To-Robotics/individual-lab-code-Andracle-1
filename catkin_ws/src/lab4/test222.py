#!/usr/bin/env python3
import sys
import rospy
import moveit_commander
import geometry_msgs.msg
import numpy as np

class PolynomialTrajectoryGenerator(object):
    def __init__(self):
        moveit_commander.roscpp_initialize(sys.argv)
        rospy.init_node('task9_polynomial_trajectory', anonymous=True)
        self.move_group = moveit_commander.MoveGroupCommander("arm")

    def generate_cubic_trajectory(self, start_pose, end_pose, tf, num_points=50):
        """
        Generates task-space waypoints using cubic polynomial interpolation.
        Equations:
        P(t) = a0 + a1*t + a2*t^2 + a3*t^3
        Boundary conditions for zero initial and final velocity:
        a0 = P0
        a1 = 0
        a2 = 3*(Pf - P0) / tf^2
        a3 = -2*(Pf - P0) / tf^3
        """
        waypoints = []
        p0 = np.array([start_pose.position.x, start_pose.position.y, start_pose.position.z])
        pf = np.array([end_pose.position.x, end_pose.position.y, end_pose.position.z])

        # Calculate cubic coefficients 
        a0 = p0
        a1 = np.zeros(3)
        a2 = 3.0 * (pf - p0) / (tf**2)
        a3 = -2.0 * (pf - p0) / (tf**3)

        # Generate points along the polynomial curve
        for i in range(num_points + 1):
            t = i * (tf / float(num_points))
            pt = a0 + a1*t + a2*(t**2) + a3*(t**3)

            pose = geometry_msgs.msg.Pose()
            pose.position.x = pt[0]
            pose.position.y = pt[1]
            pose.position.z = pt[2]
            
            # Keep orientation constant for task-space position interpolation
            pose.orientation = start_pose.orientation
            waypoints.append(pose)

        return waypoints

    def execute_polynomial_path(self, target_pose, execution_time=5.0):
        """Generates and executes the cubic polynomial path to the target pose."""
        rospy.loginfo("Generating cubic polynomial trajectory...")
        start_pose = self.move_group.get_current_pose().pose
        
        # Get the waypoints via cubic interpolation
        waypoints = self.generate_cubic_trajectory(start_pose, target_pose, execution_time)
        
        # Pass the waypoints to compute_cartesian_path
        (plan, fraction) = self.move_group.compute_cartesian_path(waypoints, 0.01, 0.0)
        
        if fraction > 0.95:
            rospy.loginfo("Trajectory planned successfully. Executing...")
            self.move_group.execute(plan, wait=True)
        else:
            rospy.logwarn(f"Failed to plan complete path. Only planned {fraction * 100:.2f}%")

if __name__ == '__main__':
    try:
        generator = PolynomialTrajectoryGenerator()
        
        # Example usage (uncomment and modify to test):
        # target_pose = geometry_msgs.msg.Pose()
        # target_pose.position.x = 0.25
        # target_pose.position.y = 0.1
        # target_pose.position.z = 0.2
        # target_pose.orientation.w = 1.0
        
        # generator.execute_polynomial_path(target_pose, execution_time=4.0)
        
    except rospy.ROSInterruptException:
        pass
