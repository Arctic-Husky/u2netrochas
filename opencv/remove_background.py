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

print("Removendo backgrounds")

images = load_images_from_folder('../test_data/test_images')
masks = load_images_from_folder('../test_data/u2net_bce_itr_15656_train_0.230484_tar_0.023406_results')

i = 0
while i < len(images):
    final = cv2.bitwise_and(images[i], masks[i])
    cv2.imwrite("../final_images/image{}.png".format(i), final)
    i = i + 1

