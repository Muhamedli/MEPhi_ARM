import roboticstoolbox as rtb
import spatialmath as sm
import spatialgeometry as sg
import swift
import numpy as np
import matplotlib.pyplot as plt

env = swift.Swift()
env.launch(realtime=True)

robot = rtb.models.MEPhI_ARM()
robot.q = robot.qz
env.add(robot)

Tep1 = robot.fkine(robot.q) * sm.SE3.Trans(0.0, 0.2, -0.1) * sm.SE3.OA([0, 0, -1], [0, 1, 0])
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

    travel_time = 5
    step = 50
    step_time = travel_time / step
    time_vec = np.arange(0, travel_time, step_time)
    traj2 = rtb.tools.trajectory.mtraj(rtb.trapezoidal, sol1[0], sol2[0], time_vec)

    # графики скоростей в осях
    graphics = traj2.qd.transpose()
    for i in range(6):
        if i != 6:
            plt.plot(graphics[i] * 180 / np.pi, label=f"{i + 1}")
    plt.legend()
    plt.show()

    for i in traj2.q:
        # goal_ax = sg.Axes(0.1, pose=robot.fkine(i))
        # env.add(goal_ax)
        robot.q = i
        env.step(step_time)
        np.set_printoptions(linewidth=100, suppress=True)
    sol1 = sol2
