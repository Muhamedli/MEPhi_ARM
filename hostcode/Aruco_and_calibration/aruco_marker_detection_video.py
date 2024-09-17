import cv2

from hostcode.taking import *

imageHight = 720
imageWidth = 1280

frameWidth = 0.50
frameHight = 0.255

# Define camera
camera = cv2.VideoCapture(0)
# camera.set(cv2.CAP_PROP_EXPOSURE, 40)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, imageWidth)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, imageHight)

while True:
    # Read image
    good, img = camera.read()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    imgToProduse = gray

    # Define ArUco detection parameters
    arucoParams = cv2.aruco.DetectorParameters()
    arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)

    # Perform ArUco marker detection
    detector = cv2.aruco.ArucoDetector(arucoDict, arucoParams)
    (corners, ids, rejected) = detector.detectMarkers(imgToProduse)
    # print(corners)
    if len(corners) != 0:
        # Display corners of marker
        # cv2.aruco.drawDetectedMarkers(img, corners, ids)
        cv2.aruco.drawDetectedMarkers(img, corners)

        # Display center of marker
        x_sum = corners[0][0][0][0] + corners[0][0][1][0] + corners[0][0][2][0] + corners[0][0][3][0]
        y_sum = corners[0][0][0][1] + corners[0][0][1][1] + corners[0][0][2][1] + corners[0][0][3][1]
        x_centerPixel = x_sum * .25
        y_centerPixel = y_sum * .25

        cv2.circle(img, (int(x_centerPixel), int(y_centerPixel)),
                   radius=5, color=(0, 255, 0), thickness=2)

        x_centerPixel_END_CS = 1 * (x_centerPixel - imageWidth / 2)
        y_centerPixel_END_CS = -1 * (y_centerPixel - imageHight / 2)

        x_centerMeter_END_CS = x_centerPixel_END_CS * frameWidth / imageWidth
        y_centerMeter_END_CS = y_centerPixel_END_CS * frameHight / imageHight

        print("x: ", round(x_centerMeter_END_CS, ndigits=3), "y: ", round(y_centerMeter_END_CS, ndigits=3))

        # Display size of the image
        # print("width: ", img.shape[1], "height: ", img.shape[0])
        # Display size of the marker
        # print(corners[0][0][1][0] - corners[0][0][0][0])
        # Display angles of joints
        font = cv2.FONT_HERSHEY_COMPLEX
        bottomLeftCornerOfText = (img.shape[1] // 8, img.shape[0] // 10)
        fontScale = 1
        fontColor = (147, 20, 255)
        thickness = 2
        lineType = 1

        angle_joint = angleArray(x_centerMeter_END_CS, y_centerMeter_END_CS)

        text = ""
        for i in range(len(angle_joint)):
            text += f"angle joint {i + 1}: {angle_joint[i]}\n"

        y0, dy = 50, 50
        for i, line in enumerate(text.split('\n')):
            y = y0 + i * dy
            cv2.putText(img, line, (50, y),
                        font,
                        fontScale,
                        fontColor,
                        thickness,
                        lineType)
    # Display image
    cv2.namedWindow("Object_detection", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Object_detection", width=imageWidth, height=imageHight)
    cv2.imshow("Object_detection", img)
    # Wait for the key press
    if cv2.waitKey(1) == ord('q'):
        break
