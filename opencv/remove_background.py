import cv2
import os

def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename))
        if img is not None:
            images.append(img)
    return images

def removeBackground(pastaImagens: str, pastaMascaras: str, pastaResultados: str, fileName: str) -> str:
    print("Removendo backgrounds")
    images = load_images_from_folder(pastaImagens)
    masks = load_images_from_folder(pastaMascaras)

    imagePath = ""

    i = 0
    while i < len(images):
        # Converte a imagem para RGBA
        alpha_channel = cv2.split(masks[i])[0]

        # Faz o canal alfa ser transparente para pixels pretos (do plano de fundo)
        alpha_channel[alpha_channel == 0] = 0

        # Adiciona o canal alfa na imagem original
        images[i] = cv2.merge([images[i], alpha_channel])


        head, _, _ = fileName.partition('.')
        cv2.imwrite(pastaResultados + "/{}.png".format(head), images[i])
        i = i + 1
        imagePath = pastaResultados + "/{}.png".format(head)
    return imagePath