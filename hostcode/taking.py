import roboticstoolbox as rtb
import spatialmath as sm
import numpy as np
from swift import Swift
import time

hight = 0.308

robot = rtb.models.MEPhI_ARM()
robot.q = robot.qz

# env = Swift()
# env.launch(realtime=True)
# env.add(robot)


def SolDimArray(tvec, trans_matrix, const_orient = True, q = robot.qr):
    sol = SolDim(tvec, trans_matrix, const_orient, q)
    robot.q = sol
    # env.step()
    sol = list(map(lambda x : round((x / np.pi * 180), ndigits=1), sol))
    return sol


def TrajFromQToPoint(tvec, trans_matrix, const_orient = True, q = robot.qr):
    sol = SolDim(tvec, trans_matrix, const_orient, q)
    traj = rtb.tools.trajectory.jtraj(q, sol, 25)
    return traj


def SolDim(tvec, trans_matrix, const_orient, q):
    new_y_axis_orientation = [-i for i in np.array(trans_matrix).transpose()[1]]
    if (const_orient == True):
        new_y_axis_orientation[2] = 0
        new_z_axis_orientation = [0, 0, 1]
    else:
        new_z_axis_orientation = [-i for i in np.array(trans_matrix).transpose()[2]]
        
    Tep = robot.fkine(q) * sm.SE3.Trans(tvec[0], tvec[1], tvec[2]) * sm.SE3.OA(new_y_axis_orientation,new_z_axis_orientation)
    sol = robot.ik_LM(Tep)

    if (chekTaskPresessing(tvec, sol[0], q)):
        return sol[0]
    else:
        print("trouble")
        return robot.q


def chekTaskPresessing(tvec, sol, q):
    tvec_env, rvec_env = FromQtoVec(q, sol)
    if (abs(tvec[2]-tvec_env[2]) + abs(tvec[0] - tvec_env[0]) + abs(tvec[1] - tvec_env[1]) < 0.005):
        return 1
    else:
        return 0

def FromQtoVec(qBeg, qEnd):
    tvec = [0, 0, 0]
    end_rmatx = [[],[],[]]
    beg_rmatx = [[],[],[]]

    for i in range(3):
        tvec[i] = ((robot.fkine(qEnd).A)[i][3] - (robot.fkine(qBeg).A)[i][3])
        beg_rmatx[i] = list((robot.fkine(qBeg).A)[i][:3])
        end_rmatx[i] = list((robot.fkine(qEnd).A)[i][:3])
    
    tvec = np.transpose(np.matmul(np.linalg.inv(np.array(beg_rmatx)), np.array(tvec).transpose()))

    trans_mtx = np.linalg.inv(np.array(end_rmatx)).dot(np.array(beg_rmatx))
    return tvec, trans_mtx

def fromQtoR():
    tvec, trans_mtx = FromQtoVec(robot.q, robot.qr)
    sol  = TrajFromQToPoint(tvec, trans_mtx, False, robot.q)
    return sol
fromQtoR()