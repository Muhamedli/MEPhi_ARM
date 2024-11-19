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

    ids, arucoIdDict, transMatrixDict, tvecDict = cvf.markers_detection()

    if ids is not None:
        for j in ids:
            index = cvf.fromArucIDtoIndex(j, arucoIdDict)

            tvecDict[index][0] -= 0.005
            tvecDict[index][1] -= 0.03
            tvecDict[index][2] -= (0.0562 + 0.034)

            transMatrixDict[index][1] = [-i for i in np.array(transMatrixDict[index][0])[1]]
            transMatrixDict[index][2] = [-i for i in np.array(transMatrixDict[index][0])[2]]

    cvf.imgDrawing()
    return ids, arucoIdDict, transMatrixDict, tvecDict


def trajectoryPlanning(ids, arucoIdDict, tvecDict):
    rvecsTraj = None
    if ids is not None:
        rvecsArray = [[0]*len(ids) for i in range(len(ids))]
        for i in ids:
            for j in ids:
                rvec = np.array(tvecDict[cvf.fromArucIDtoIndex(j, arucoIdDict)]) - np.array(tvecDict[cvf.fromArucIDtoIndex(i, arucoIdDict)])
                rvecsArray[cvf.fromArucIDtoIndex(i, arucoIdDict)][cvf.fromArucIDtoIndex(j, arucoIdDict)] = rvec
                rvecsArray[cvf.fromArucIDtoIndex(j, arucoIdDict)][cvf.fromArucIDtoIndex(i, arucoIdDict)] = rvec * -1
    
        minMagnSum =  0
        minId = 0
        for i in ids:
            magnSum = sum(list(map(np.linalg.norm(), rvecsArray[cvf.fromArucIDtoIndex(i, arucoIdDict)])))
            if magnSum<minMagnSum:
                minMagnSum = magnSum
                minId = i
        
        rvecsTraj = [tvecDict[cvf.fromArucIDtoIndex(minId, arucoIdDict)]]

        for i in range(len(ids)):
            rvecsTraj.append(rvecsArray[cvf.fromArucIDtoIndex(minId, arucoIdDict)][i] - np.array([0,0, 0.25 * i]))
            rvecsTraj.append(rvecsArray[i][cvf.fromArucIDtoIndex(minId, arucoIdDict)] + np.array([0,0, 0.25 * (i+1)]))
            
    return rvecsTraj


while(1):
    ids, arucoIdDict, transMatrixDict, tvecDict = imgProdussing()
    rvecsTraj = trajectoryPlanning(ids, arucoIdDict, tvecDict)
    for rvec in rvecsTraj:
        traj = tk.jtrajFromCurToGiven(tk.SolFinder(rvec, np.eye(3), q = tk.robot.q))
        sp.sendTraj(traj)

