import roboticstoolbox as rtb
import spatialmath as sm
import numpy as np
from swift import Swift
import spatialgeometry as sg

# Make and instance of the Swift simulator and open it
env = Swift()
env.launch(realtime=True)

# Make a panda model and set its joint angles to the ready joint configuration
panda = rtb.models.MEPhI_ARM()
panda.q = panda.qr

# Set a desired and effector pose an an offset from the current end-effector pose
Tep = panda.fkine(panda.q) * sm.SE3.Trans(0, 0.28, 0) * sm.SE3.OA([0, 1, 0], [0, 0, 1])
goal_ax = sg.Axes(0.1, pose=Tep)

# Add the robot to the simulator
env.add(panda)
env.add(goal_ax)

# Simulate the robot while it has not arrived at the goal
arrived = False
while not arrived:
    # Work out the required end-effector velocity to go towards the goal
    v, arrived = rtb.p_servo(panda.fkine(panda.q), Tep, 1)

    # Set the Panda's joint velocities
    panda.qd = np.linalg.pinv(panda.jacobe(panda.q)) @ v

    # Step the simulator by 50 milliseconds
    env.step(0.01)
