import cv2
import numpy as np
import glob
import json
import os

ARUCO_DICT = cv2.aruco.DICT_5X5_1000  # Dictionary ID
SQUARES_VERTICALLY = 6  # Number of squares vertically
SQUARES_HORIZONTALLY = 9  # Number of squares horizontally
SQUARE_LENGTH = 64  # Square side length (in pixels)
MARKER_LENGTH = 48  # ArUco marker side length (in pixels)
MARGIN_PX = 20  # Margins size (in pixels)


def get_calibration_parameters(img_dir):
    # Define the aruco dictionary, charuco board and detector
    dictionary = cv2.aruco.getPredefinedDictionary(ARUCO_DICT)
    board = cv2.aruco.CharucoBoard((SQUARES_HORIZONTALLY, SQUARES_VERTICALLY), SQUARE_LENGTH, MARKER_LENGTH, dictionary)
    board.setLegacyPattern(True)
    params = cv2.aruco.DetectorParameters()
    detector = cv2.aruco.ArucoDetector(dictionary, params)

    # Возможно придется указать полный путь к файлу
    image_files = glob.glob('samples_charuco/*.jpg')

    all_charuco_ids = []
    all_charuco_corners = []

    # Loop over images and extraction of corners
    for image_file in image_files:
        image = cv2.imread(image_file)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        imgSize = image.shape
        image_copy = image.copy()
        marker_corners, marker_ids, rejectedCandidates = detector.detectMarkers(image)

        if len(marker_ids) > 0:  # If at least one marker is detected
            cv2.aruco.drawDetectedMarkers(image_copy, marker_corners, marker_ids)
            ret, charucoCorners, charucoIds = cv2.aruco.interpolateCornersCharuco(marker_corners, marker_ids, image,
                                                                                  board)
            print(charucoCorners)
            if charucoIds is not None and len(charucoCorners) > 3:
                all_charuco_corners.append(charucoCorners)
                all_charuco_ids.append(charucoIds)
                print("hello")

    # Calibrate camera with extracted information
    result, mtx, dist, rvecs, tvecs = cv2.aruco.calibrateCameraCharuco(all_charuco_corners, all_charuco_ids, board,
                                                                       imgSize, None, None)
    return mtx, dist


OUTPUT_JSON = 'charuco_board_calibration.json'

mtx, dist = get_calibration_parameters(img_dir='samples_charuco')
data = {"camera_matrix": mtx.tolist(), "dist_coeff": dist.tolist()}

with open(OUTPUT_JSON, 'w') as json_file:
    json.dump(data, json_file, indent=4)