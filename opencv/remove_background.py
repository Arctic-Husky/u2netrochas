import cv2
import os
from pathlib import Path

# opencv loads the image in BGR, convert it to RGB
def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename))
        if img is not None:
            images.append(img)
    return images



images = load_images_from_folder('Images')
masks = load_images_from_folder('Masks')

i = 0
while i < len(images):
    final = cv2.bitwise_and(images[i], masks[i])
    cv2.imwrite("Final_Images/{}.png".format(i), final)
    i = i + 1

