import cv2
import numpy as np
from datetime import datetime


<<<<<<< HEAD

#camera = cv2.VideoCapture(2) # 0 webcam, 2 external
=======
>>>>>>> dfd652eaa8b13a1137d34cd52d24ea666d1438ef
camera = cv2.VideoCapture(1)

width, height = 1280, 720

camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)


while True:
    __, frame = camera.read()
<<<<<<< HEAD
    frame_copy = np.copy(frame)
    cv2.rectangle(frame, (280, 0), (1000, 719), (0,0,255), thickness=3)
    cv2.imshow("camera", cv2.pyrDown(frame))
=======
>>>>>>> dfd652eaa8b13a1137d34cd52d24ea666d1438ef
    cv2.imshow("camera", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if cv2.waitKey(1) & 0xFF == ord('s'):
        cv2.imwrite(f"calibration_images/photo-{datetime.now().strftime('%H-%M-%S')}.png", frame_copy[:, 280:1000])

        print(datetime.now().strftime("%H:%M:%S"))