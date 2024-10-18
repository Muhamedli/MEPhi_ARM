import cv2
import traj_planning as tk
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
    try:
        ids, tvec, rvec = cvf.markers_detection()

        if ids is not None:

            for j in range(len(ids)):
                for i in range(len(tvec[0][0])):
                    filValTvec[i] = RunningAverageAdaptive(tvec[0][0][i], filValTvec[i])

                tvec[0][0] = filValTvec

                tvec[0][0][0] -= 0.005
                tvec[0][0][1] -= 0.03
                tvec[0][0][2] -= (0.0562 + 0.034)

                trans_matrix = cv2.Rodrigues(rvec)

                trans_matrix[0][1] = [-i for i in np.array(trans_matrix[0])[1]]
                trans_matrix[0][2] = [-i for i in np.array(trans_matrix[0])[2]]

    except:
        print("trouble")

    cvf.imgDrawing()

    return ids, rvec, tvec
