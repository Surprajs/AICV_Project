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

images = glob("outputs/*.png")

for image in images:
    img_color = cv2.imread(image)
    img_gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)

    status, corners = cv2.findChessboardCorners(img_gray, chess, None)

    if status:
        objpoints.append(objp)
        cv2.cornerSubPix(img_gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners)

        cv2.drawChessboardCorners(img_color, chess, corners, status)
        # cv2.imshow('img', img_color)
        filename = os.path.basename(image).rsplit('.',1)[0]
        # cv2.imwrite(f"outputs/{filename}-corners.png", img_color)
        cv2.waitKey(1000)

ret, mtx, dist, __, __ = cv2.calibrateCamera(objpoints, imgpoints, img_gray.shape[::-1], None, None)

print(ret)
print(mtx)
print(dist)


with open("camera_parameters.npz", mode="wb") as file:
    np.savez(file, ret=ret,mtx=mtx,dist=dist)

"""
for image in images:
    img = cv2.imread(image)
    h,w = img.shape[:2]
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx,dist, (w,h), 1, (w,h))
    dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
    # print(img.shape)
    # print(dst.shape)
    cv2.imshow(f"{image}", dst)
    # saving the images in PNG format
    # filename = os.path.basename(image).rsplit('.',1)[0]
    # cv2.imwrite(f"und/und_{filename}_2.png", dst)
    # cv2.imwrite(f"und/png_{filename}.png", image)
"""
cv2.waitKey(0)
cv2.destroyAllWindows()