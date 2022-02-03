import cv2
import numpy as np
from datetime import datetime


camera = cv2.VideoCapture(0)

width, height = 1280, 720

camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)


while True:
    __, frame = camera.read()
    frame_copy = np.copy(frame)
    cv2.imshow("camera", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if cv2.waitKey(1) & 0xFF == ord('s'):
        cv2.imwrite(f"calibration_images/photo-{datetime.now().strftime('%H-%M-%S')}.png", frame) #frame_copy[:, 280:1000])
        print(datetime.now().strftime("%H:%M:%S"))