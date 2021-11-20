import cv2
import numpy as np

camera = cv2.VideoCapture(1)

width, height = 1280,720
# width, height = 1920,1080

camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

with np.load("camera_parameters_0.npz") as file:
    ret, mtx, dist = file["ret"], file["mtx"], file["dist"]
print(ret,mtx,dist)
with np.load("camera_parameters_0.npz") as file:
    ret, mtx, dist = file["ret"], file["mtx"], file["dist"]
print(ret,mtx,dist)

newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx,dist, (width,height), 1, (width,height))

while True:
    __, frame = camera.read()
    dst = cv2.undistort(frame,mtx,dist,None,newcameramtx)
    cv2.imshow("camera", cv2.hconcat([cv2.pyrDown(frame),cv2.pyrDown(dst)]))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
