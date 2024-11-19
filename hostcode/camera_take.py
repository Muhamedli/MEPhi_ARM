import traj_planning as tk
import keyboard
import cv_functions as cvf
import numpy as np
import serial_port as sp

flag = 1
fPressed = 0

cvf.camera_initialisation()

sp.serialBegin()

def imgProdussing():
    cvf.video_capture()

    ids, transMatrixDict, tvecDict = cvf.markers_detection()

    if ids is not None:
        for j in ids:
            tvecDict[j][0] -= 0.005
            tvecDict[j][1] -= 0.03
            tvecDict[j][2] -= (0.0562 + 0.034)

            transMatrixDict[j][1] = [-i for i in np.array(transMatrixDict[j])[1]]
            transMatrixDict[j][2] = [-i for i in np.array(transMatrixDict[j])[2]]

    cvf.imgDrawing()
    return ids, transMatrixDict, tvecDict


def trajectoryPlanning(ids, tvecDict):
    tvecsTraj = None
    if ids is not None:
        tvecsTraj = [np.array([0,0,0])]
        for id in ids:
            tvecsTraj.append(tvecDict[id]-tvecsTraj[-1])
        tvecsTraj = tvecsTraj[1:]

    return tvecsTraj   

traj = tk.jtrajFromCurToGiven(tk.robot.qr)
sp.sendTraj(traj)


ids, transMatrixDict, tvecDict = imgProdussing()
tvecsTraj = trajectoryPlanning(ids, tvecDict)
if tvecsTraj is not None:
    for tvec in tvecsTraj:
        traj = tk.jtrajFromCurToGiven(tk.SolFinder(tvec, np.eye(3), q = tk.robot.q))
        if traj is not None:
            sp.sendTraj(traj)
        else:
            break

