import time

import roboticstoolbox as rtb
import spatialmath as sm
import spatialgeometry as sg
import swift
import numpy as np

env = swift.Swift()
env.launch(realtime=True)

robot = rtb.models.MEPhI_ARM()
robot.q = robot.qr
env.add(robot)

Tep1 = robot.fkine(robot.q) * sm.SE3.Trans(0, 0, 0.2) * sm.SE3.OA([0, 1, 0], [0, 0, 1])
sol1 = robot.ik_LM(Tep1)
goal_ax = sg.Axes(0.1, pose=Tep1)
env.add(goal_ax)
traj1 = rtb.tools.trajectory.jtraj(robot.qz, sol1[0], 100)
# print(traj1.q)
for i in traj1.q:  # for each joint configuration on trajectory
    robot.q = i  # update the robot state
    env.step(0.01)  # update visualization

gripper = robot.grippers[0]
for i in range(0, 38):  # Moving gripper
    # print(i)
    gripper.q = [i / 1000]
    env.step(0.01)
time.sleep(3)
for i in range(0, 38):  # Moving gripper
    # print(i)
    gripper.q = [(37 - i) / 1000]
    env.step(0.01)
