import cv2
from taking import *
import json

f = open("Aruco_and_calibration/charuco_board_calibration.json")
data = json.load(f)

imageHight = 1080
imageWidth = 1920

camera_matrix = np.array(data["camera_matrix"])
dist_coefs = np.array(data["dist_coeff"])
newcameramtx, roi = cv2.getOptimalNewCameraMatrix(camera_matrix, dist_coefs, (imageWidth, imageHight), 1,
                                                  (imageWidth, imageHight))

flag = 1
fPressed = 0
text = ""
y0, dy = 50, 50

font = cv2.FONT_HERSHEY_COMPLEX
fontScale = 1
fontColor = (147, 20, 255)
thickness = 2
lineType = 1

camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, imageWidth)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, imageHight)

tvecArray = []
filVal = [0, 0, 0]


def RunningAverageAdaptive(newVal, filVal):
    if (abs(newVal - filVal) > 1.5):
        k = 1.5
    else:
        k = 0.5

    filVal += (newVal - filVal) * k
    return filVal


while True:
    good, img = camera.read()

    img = cv2.undistort(img, camera_matrix, dist_coefs, None, newcameramtx)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgToProduse = gray

    arucoParams = cv2.aruco.DetectorParameters()
    arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)
    detector = cv2.aruco.ArucoDetector(arucoDict, arucoParams)
    (corners, ids, rejected) = detector.detectMarkers(imgToProduse)
    if len(corners) != 0:
        try:
            rvec, tvec, _objPoints = cv2.aruco.estimatePoseSingleMarkers(corners, 0.025, camera_matrix, dist_coefs)
            cv2.drawFrameAxes(img, camera_matrix, dist_coefs, rvec, tvec, length=0.025)
            for i in range(len(tvec[0][0])):
                filVal[i] = RunningAverageAdaptive(tvec[0][0][i], filVal[i])
                tvec[0][0][i] = filVal[i]
        except:
            print("trouble")
        cv2.aruco.drawDetectedMarkers(img, corners)

        # print(list(map(lambda x: round(x/np.pi * 180), rvec[0][0])))

        tvec[0][0][2] -= 0.085  # 0.308

        ''''
        # tvec[0][0][2] = 0.308
        tvec[0][0][1] = tvec[0][0][1] - 0.0325
        tvec[0][0][0] -= 0.01
        '''

        if (flag):
            angle_joint = SolDimArray(tvec[0][0])

        text = ""
        for i in range(len(angle_joint)):
            text += f"angle joint {i + 1}: {angle_joint[i]}\n"

    # Display image
    for i, line in enumerate(text.split('\n')):
        y = y0 + i * dy
        cv2.putText(img, line, (50, y),
                    font,
                    fontScale,
                    fontColor,
                    thickness,
                    lineType)

    cv2.namedWindow("Object_detection", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Object_detection", width=imageWidth, height=imageHight)
    cv2.imshow("Object_detection", img)

    # Wait for the key press

    if cv2.waitKey(1) == ord('f'):
        if fPressed == 0:
            flag = (flag + 1) % 2
            fPressed = 1
    elif fPressed == 1:
        fPressed = 0

    if cv2.waitKey(1) == ord('q'):
        break
