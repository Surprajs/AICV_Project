from glob import glob
from os import path

from BoardRecognition import BoardRecognition


b1 = BoardRecognition()

images = glob("board_images/*.png")

for file in images:
    filename = path.basename(file).rsplit('.',1)[0]
    image = b1.load_image(file)
    points = b1.get_points(image)
    b1.crop_squares(image, points, filename, True)
    print(filename)
