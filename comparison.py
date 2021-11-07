import cv2
import numpy as np
from datetime import datetime


camera = cv2.VideoCapture(0)

width, height = 1280,720
camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

with np.load("camera_parameters.npz") as file:
    ret, mtx, dist = file["ret"], file["mtx"], file["dist"]
    # ret = file["ret"]
newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx,dist, (width,height), 1, (width,height))
# print(ret)
# print(mtx)
# print(dist)

counter = 0
while True:
    __, frame = camera.read()
    dst = cv2.undistort(frame,mtx,dist,None,newcameramtx)
    cv2.imshow("camera", cv2.hconcat([cv2.pyrDown(frame),cv2.pyrDown(dst)]))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if cv2.waitKey(1) & 0xFF == ord('s'):
        cv2.imwrite(f"outputs/photo-{counter}.png", frame)
        counter+=1
        print(datetime.now().strftime("%H:%M:%S"))