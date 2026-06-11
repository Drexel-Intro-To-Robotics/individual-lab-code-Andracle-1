import numpy as np

class OpenManipulatorKinematics:
    def __init__(self):
        # OpenManipulator-X Link Lengths in meters
        self.L1 = 0.0775  # Base to Joint 2 height (Z)
        self.L2 = 0.1300  # Joint 2 to Joint 3 length
        self.L3 = 0.1240  # Joint 3 to Joint 4 length
        self.L4 = 0.1260  # Joint 4 to Gripper tool center point (TCP)

    def forward_kinematics(self, joints):
        
        #Calculates the end-effector (TCP) position (x, y, z) based on 4 joint angles.
        #Angles expected in radians.
        
        q1, q2, q3, q4 = joints

        # Projecting the arm length onto the ground plane
        r = self.L2 * np.cos(q2) + self.L3 * np.cos(q2 + q3) + self.L4 * np.cos(q2 + q3 + q4)
        
        # Absolute coordinates relative to base frame 
        x = r * np.cos(q1)
        y = r * np.sin(q1)
        z = self.L1 + self.L2 * np.sin(q2) + self.L3 * np.sin(q2 + q3) + self.L4 * np.sin(q2 + q3 + q4)
        
        return np.array([x, y, z])

    def inverse_kinematics(self, target_pos):
        
        #Analytically solves IK for a desired (x, y, z) position using trigonometry.
        
        x, y, z = target_pos

        q1 = np.arctan2(y, x)

        r = np.sqrt(x**2 + y**2)
        
        r_eff = r - self.L4
        z_eff = z - self.L1

        D = (r_eff**2 + z_eff**2 - self.L2**2 - self.L3**2) / (2 * self.L2 * self.L3)
        
        D = np.clip(D, -1.0, 1.0)
        
        # Elbow-up configuration (-), use (+) for elbow-down
        q3 = -np.arccos(D)

       
        theta1 = np.arctan2(z_eff, r_eff)
        theta2 = np.arctan2(self.L3 * np.sin(q3), self.L2 + self.L3 * np.cos(q3))
        q2 = theta1 - theta2

        
        q4 = 0.0 - q2 - q3

        return np.array([q1, q2, q3, q4])


if __name__ == "__main__":
    solver = OpenManipulatorKinematics()

    # 1. Define three reachable target end-effector poses (X, Y, Z in meters)
    target_poses = [
        np.array([-0.0821, 0.3432, 0.1917]),   # Target 1
        np.array([-0.1112, -0.3373, -0.032]),  # Target 2
        np.array([0.2269, 0.2922, 0.1483])  # Target 3
    ]

    print("  OPENMANIPULATOR-X GEOMETRIC KINEMATICS SOLVER   ")

    for i, target in enumerate(target_poses, 1):
        print(f"--- POSE {i} ---") 
        print(f"Target Position (X, Y, Z): {target} meters")
        
        # Solve Inverse Kinematics
        joint_angles = solver.inverse_kinematics(target)
        print(f"Solved Joint Angles (q1, q2, q3, q4):\n  {np.round(joint_angles, 4)} rad")
        print(f"  {np.round(np.degrees(joint_angles), 2)} deg")
        
        # Verify using Forward Kinematics
        verified_pos = solver.forward_kinematics(joint_angles)
        print(f"FK Verification Position:   {np.round(verified_pos, 4)}")
        
        # Compute tracking error
        error = np.linalg.norm(target - verified_pos)
        print(f"Absolute Position Error:    {error:.6f} meters") 
        print("\n" + "-"*50 + "\n")
