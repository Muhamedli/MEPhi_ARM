import cv2

focus = 0
imageHight = 1080
imageWidth = 1920

camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, imageWidth)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, imageHight)
camera.set(28, focus)

while True:
    good, img = camera.read()

    cv2.namedWindow("camera_focus", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("camera_focus", width=imageWidth, height=imageHight)
    cv2.imshow("camera_focus", img)

    if cv2.waitKey(1) == ord('q'):
        break
