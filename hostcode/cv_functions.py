import cv2
import numpy as np
import json


def camera_initialisation(cameraID = 0, imageWidth = 1920, imageHight = 1080):
    global camera, newcameramtx, camera_matrix, dist_coefs, detector

    f = open("Aruco_and_calibration/charuco_board_calibration.json")
    data = json.load(f)

    camera_matrix = np.array(data["camera_matrix"])
    dist_coefs = np.array(data["dist_coeff"])
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(camera_matrix, dist_coefs, (imageWidth, imageHight), 1, (imageWidth, imageHight))

    camera = cv2.VideoCapture(cameraID, cv2.CAP_DSHOW)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, imageWidth+10)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, imageHight+10)

    arucoParams = cv2.aruco.DetectorParameters()
    arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)
    detector = cv2.aruco.ArucoDetector(arucoDict, arucoParams)

def video_capture():
    global img, imgToProduse

    good, img = camera.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgToProduse = gray

def markers_detection():
    (corners, ids, rejected) = detector.detectMarkers(imgToProduse)
    if ids is not None:
        rvec, tvec, _objPoints = cv2.aruco.estimatePoseSingleMarkers(corners, 0.025, camera_matrix, dist_coefs)
        cv2.drawFrameAxes(img, camera_matrix, dist_coefs, rvec, tvec, length=0.025)
        return ids, rvec, tvec
        cv2.aruco.drawDetectedMarkers(img, corners)

def imgDrawing(imageWidth = 720, imageHight = 480):

    cv2.namedWindow("Object_detection", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Object_detection", width=imageWidth, height=imageHight)
    cv2.imshow("Object_detection", img)
    cv2.waitKey(1)

