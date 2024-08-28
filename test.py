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
# print(traj1.q)
for i in traj1.q:  # for each joint configuration on trajectory
    robot.q = i  # update the robot state
    env.step(0.01)  # update visualization

Tep2 = robot.fkine(robot.q) * sm.SE3.Trans(0.2, 0, 0) * sm.SE3.OA([0, 1, 0], [0, 0, 1])  # Задание целевой позы
goal_ax = sg.Axes(0.1, pose=Tep2)  # построение системы координат в ней
env.add(goal_ax)
step = 25  # кол-во точек разбиения траектории
time = 1  # время прохождения траектории
time_point_interval = time / step
traj2 = rtb.tools.trajectory.ctraj(Tep1, Tep2, step)  # построение траектории
cartesian_sol = robot.ikine_LM(traj2)  # получение обобщенных координат каждой точки траектории

velocity_array = np.empty((step, 6))
for i in range(step - 1):
    for k in range(6):
        velocity_array[i][k] = (cartesian_sol.q[i + 1][k] - cartesian_sol.q[i][
            k]) / time_point_interval  # вычисление обобщенных скоростей в осях для каждой точки траектории
np.set_printoptions(precision=3, linewidth=100, suppress=True)
print(velocity_array)

for i in cartesian_sol.q:
    # goal_ax = sg.Axes(0.1, pose=robot.fkine(i))
    # env.add(goal_ax)
    robot.q = i
    env.step(0.01)
