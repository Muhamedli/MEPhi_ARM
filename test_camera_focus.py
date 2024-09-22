import cv2

focus = 0

camera = cv2.VideoCapture(0)
camera.set(28, focus)

while True:
    good, img = camera.read()
    cv2.namedWindow("camera_focus", cv2.WINDOW_NORMAL)
    cv2.imshow("camera_focus", img)
    if cv2.waitKey(1) == ord('q'):
        break
