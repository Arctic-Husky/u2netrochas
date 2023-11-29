import os
from u2net_test import makeMask

def doMakeMask(imagePath: str, resultsDir: str):
    """
    Utiliza o u2net_test para produzir a máscara da imagem passada

    @param str modelName: nome do modelo a ser utilizado
    @param
    @param
    """
    makeMask(imagePath, resultsDir)

def getMask(modelName: str, imageName: str) -> str:
    """
    Pega o caminho para a máscara por nome

    @param str modelName: nome do modelo utilizado
    @param str imageName: nome da imagem original
    """
    #masksDir = os.path.join(os.getcwd(), 'test_data', modelName + '_results' + os.sep)
    #image = find(imageName, masksDir)
    #return image
    pass

def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)