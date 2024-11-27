import traj_planning as tk
import cv_functions as cvf
import numpy as np
import serial_port as sp
import time

flag = 1
fPressed = 0

cvf.camera_initialisation()

sp.serialBegin()

def imgProdussing():
    cvf.video_capture()

    ids, transMatrixDict, tvecDict = cvf.markers_detection()

    if ids is not None:
        for id in ids:
            for tvec in tvecDict[id]:
                tvec -= np.array([0.005, 0.03, (0.0562 + 0.034)])

            for transMatrix in transMatrixDict[id]:
                transMatrix[1] = [-i for i in np.array(transMatrix)[1]]
                transMatrix[2] = [-i for i in np.array(transMatrix)[2]]

    cvf.imgDrawing()
    return ids, transMatrixDict, tvecDict


def trajectoryPlanning(ids, tvecDict, transMatrixDict):

    drop_pose = tk.SolFinder(np.array([0.3,0.1,-0.3]), np.eye(3), q = tk.robot.qr)
    
    tvecsTraj = None
    tMatrixTraj = None
    if ids is not None:
        tvecsTraj = [np.array([0,0,0])]
        tMatrixTraj = [np.eye(3)]
        for id in ids:
            for tvec in tvecDict[id]:
                tvecsTraj.append(tvec-tvecsTraj[-1])
                tvecsTraj.append(tk.FromQtoVec(drop_pose)[0] - tvec)
            for tMatrix in transMatrixDict[id]:
                tMatrixTraj.append(np.linalg.inv(tMatrix))
                tMatexesTraj.append(tMatrix)


        tvecsTraj = tvecsTraj[1:]

    return tvecsTraj, tMatrixTraj

traj = tk.jtrajFromCurToGiven(tk.robot.qr)
sp.sendTraj(traj)

tvecsTraj = None

while tvecsTraj is None:
    ids, transMatrixDict, tvecDict = imgProdussing()
    tvecsTraj, tMatexesTraj = trajectoryPlanning(ids, tvecDict, transMatrixDict)

for i in range(len(tvecsTraj)):
    traj = tk.ctrajFromCurToGiven(tk.SolFinder(tvecsTraj[i], tMatexesTraj[i], q = tk.robot.q))
    if traj is not None:
        sp.sendTraj(traj)
    else:
        break

traj = tk.ctrajFromCurToGiven(tk.robot.qz)
sp.sendTraj(traj)
