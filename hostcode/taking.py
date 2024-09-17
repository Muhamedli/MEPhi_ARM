import roboticstoolbox as rtb
import spatialmath as sm
import numpy as np

hight = 0.308

robot = rtb.models.MEPhI_ARM()
robot.q = robot.qr


def TrajToSurf(x, y):
    Tep = robot.fkine(robot.q) * sm.SE3.Trans(x, hight, y)
    sol = robot.ik_LM(Tep)

    traj = rtb.tools.trajectory.jtraj(robot.qz, sol[0], 100)
    return traj, Tep


def SolAtSurf(x, y):
    Tep = robot.fkine(robot.q) * sm.SE3.Trans(x, hight, y)
    sol = robot.ik_LM(Tep)

    return sol[0]


def AnglePrint(x, y):
    sol = SolAtSurf(x, y)
    for i in range(len(sol)):
        print(f"{i} Joint angle is {round(sol[i] / np.pi * 180, ndigits=1)}")


def angleArray(x, y):
    sol = SolAtSurf(x, y)
    for i in range(len(sol)):
        sol[i] = round(sol[i] / np.pi * 180, ndigits=1)
    return sol
