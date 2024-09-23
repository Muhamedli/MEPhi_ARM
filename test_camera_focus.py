import cv2

focus = 200
# хз как это работает)))
imageHight = 2000
imageWidth = 2000

camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, imageHight)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, imageWidth)
camera.set(cv2.CAP_PROP_FOCUS, focus)

while True:
    good, img = camera.read()

    cv2.namedWindow("camera_focus", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("camera_focus", width=1920, height=1080)
    cv2.imshow("camera_focus", img)

    if cv2.waitKey(1) == ord('q'):
        break
