import roboticstoolbox as rtb
import spatialmath as sm
import spatialgeometry as sg
import swift
import numpy as np

env = swift.Swift()
env.launch(realtime=True)

robot = rtb.models.Puma560()
robot.q = robot.qz
env.add(robot)

Tep1 = robot.fkine(robot.q) * sm.SE3.Trans(0, -0.1, -0.2) * sm.SE3.OA([0, 0, -1], [0, 1, 0])
sol1 = robot.ik_LM(Tep1)
goal_ax = sg.Axes(0.1, pose=Tep1)
env.add(goal_ax)
traj1 = rtb.tools.trajectory.jtraj(robot.qz, sol1[0], 100)
for i in traj1.q:  # for each joint configuration on trajectory
    robot.q = i  # update the robot state
    env.step(0.01)  # update visualization

array = [[0.2, 0, 0], [0, 0, 0.2], [-0.2, 0, 0], [0, 0, -0.2]]

for el in array:
    Tep2 = robot.fkine(robot.q) * sm.SE3.Trans(el) * sm.SE3.OA([0, 1, 0], [0, 0, 1])
    sol2 = robot.ik_LM(Tep2)
    goal_ax = sg.Axes(0.1, pose=Tep2)
    env.add(goal_ax)
    traj2 = rtb.tools.trajectory.mtraj(rtb.trapezoidal, sol1[0], sol2[0], 25)
    for i in traj2.q:
        goal_ax = sg.Axes(0.1, pose=robot.fkine(i))
        env.add(goal_ax)
        robot.q = i
        env.step(0.02)
        np.set_printoptions(linewidth=100, suppress=True)
        print(traj2.qd)
    sol1 = sol2
