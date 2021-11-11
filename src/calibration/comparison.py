import cv2
import numpy as np

camera = cv2.VideoCapture(0)

width, height = 1280,720
camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

with np.load("camera_parameters.npz") as file:
    ret, mtx, dist = file["ret"], file["mtx"], file["dist"]

newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx,dist, (width,height), 1, (width,height))

counter = 0
while True:
    __, frame = camera.read()
    dst = cv2.undistort(frame,mtx,dist,None,newcameramtx)
    cv2.imshow("camera", cv2.hconcat([cv2.pyrDown(frame),cv2.pyrDown(dst)]))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break