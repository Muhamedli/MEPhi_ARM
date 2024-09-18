import roboticstoolbox as rtb
import spatialmath as sm
import numpy as np
from swift import Swift

hight = 0.308

robot = rtb.models.MEPhI_ARM()
robot.q = robot.qr

env = Swift()
env.launch(realtime=True)
env.add(robot)


def TrajToSurf(x, y):
    Tep = robot.fkine(robot.qr) * sm.SE3.Trans(x, hight, y)
    sol = robot.ik_LM(Tep)

    traj = rtb.tools.trajectory.jtraj(robot.qz, sol[0], 100)
    return traj, Tep


def SolDim(tvec):
    Tep = robot.fkine(robot.qr) * sm.SE3.Trans(tvec[0], tvec[2], tvec[1])
    sol = robot.ik_LM(Tep)
    return sol[0]


def SolDimArray(tvec):
    # sol = SolDim(list(map(lambda x: round(x, ndigits = 4),tvec)))
    sol = SolDim(tvec)
    robot.q = sol
    env.step()
    for i in range(len(sol)):
        sol[i] = round((sol[i] / np.pi * 180), ndigits=1)
    return sol
