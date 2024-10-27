import cv2
# import traj_planning as tk
import keyboard
import cv_functions as cvf
import numpy as np

flag = 1
fPressed = 0

cvf.camera_initialisation()

filValTvec = [0, 0, 0]




def RunningAverageAdaptive(newVal, filVal):
    if (abs(newVal - filVal) > 1.5):
        k = 1.5
    else:
        k = 0.2

    filVal += (newVal - filVal) * k
    return filVal


def imgProdussing():
    cvf.video_capture()

    ids, arucoIdDict, rvecDict, tvecDict = cvf.markers_detection()
    transMatrixDict = {}

    if ids is not None:
        for j in range(len(ids)):
            index = arucoIdDict[ids[j][0]]

            # for i in range(len(tvecArray[j][0][0])):
            #     filValTvec[i] = RunningAverageAdaptive(tvecArray[index][0][0][i], filValTvec[i])

            # tvecDictionary[index][0][0] = filValTvec

            tvecDict[index][0][0][0] -= 0.005
            tvecDict[index][0][0][1] -= 0.03
            tvecDict[index][0][0][2] -= (0.0562 + 0.034)

            transMatrixDict[index] = cv2.Rodrigues(rvecDict[index])

            transMatrixDict[index][0][1] = [-i for i in np.array(transMatrixDict[index][0])[1]]
            transMatrixDict[index][0][2] = [-i for i in np.array(transMatrixDict[index][0])[2]]


    cvf.imgDrawing()


while(1):
    imgProdussing()