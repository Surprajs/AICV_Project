import numpy as np
import cv2
from glob import glob
import os

chess = (13,9) # number of internal corners # (13,9)

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

objp = np.zeros((chess[0]*chess[1],3), np.float32)
objp[:,:2] = np.mgrid[0:chess[0],0:chess[1]].T.reshape(-1,2)
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

images = glob("calibration_images/*.png")

for image in images:
    img_color = cv2.imread(image)
    img_gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)
    print(image)

    status, corners = cv2.findChessboardCorners(img_gray, chess, None)

    if status:
        objpoints.append(objp)
        cv2.cornerSubPix(img_gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners)

        cv2.drawChessboardCorners(img_color, chess, corners, status)
        cv2.imshow('img', img_color)
        cv2.imwrite(f'a-{os.path.basename(image)}', img_color)
        # filename = os.path.basename(image).rsplit('.',1)[0]
        cv2.waitKey(1000)

ret, mtx, dist, __, __ = cv2.calibrateCamera(objpoints, imgpoints, img_gray.shape[::-1], None, None)

print(ret)
print(mtx)
print(dist)

with open("camera_parameters_1.npz", mode="wb") as file:
    np.savez(file, ret=ret,mtx=mtx,dist=dist)

cv2.waitKey(0)
cv2.destroyAllWindows()