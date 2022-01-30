import cv2
from glob import glob
from os import path

from BoardRecognition import BoardRecognition


b1 = BoardRecognition()

images = glob("board-22.png")

for file in images:
    filename = path.basename(file).rsplit('.',1)[0]
    print(filename)
    image = b1.load_image(file)
    points = b1.get_points(image)
    # b1.draw_points(image, points, filename)
    b1.crop_squares(image, points, filename)
cv2.waitKey(0)
cv2.destroyAllWindows()