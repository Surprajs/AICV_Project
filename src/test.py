import tensorflow as tf
import cv2
import numpy as np
from glob import glob

labels = ["black", "black_king", "empty", "white", "white_king"]
model = tf.keras.models.load_model("new_new_model")

images = glob("squares/testing/*.png")
print(images)
for image in images:
    original_image = cv2.imread(image)
    img = cv2.resize(original_image, (224,224))
    img = np.array(img)/255.0
    img = img[np.newaxis, ...]
    predicted = model.predict(img)[0]
    idx = predicted.argmax()
    cv2.imshow(f"{np.max(predicted)} {labels[idx]}", original_image)
    # else:
    #     cv2.imshow(f"{np.max(predicted)} empty", original_image)


cv2.waitKey(0)
cv2.destroyAllWindows()