from typing import Union

from fastapi import FastAPI, UploadFile
from fastapi.exceptions import HTTPException
from PIL import Image

from pydantic import BaseModel

import json
import uuid
import io
import os

import u2net.get_mask ## descobrir como importa diretamente o get_mask

PASTA_IMAGENS_RECEBIDAS = "../imagens_recebidas"

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

# class Rocha(BaseModel):
#     id: uuid
#     nome_arquivo: str
#     url_arquivo: str

# Banco: Supabase https://supabase.com/dashboard/project/yjdjcvftedrffiiidcyb


@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.post("/upload")
async def upload_file(file: UploadFile):
    if file.content_type != "image/jpeg":
        raise HTTPException(400, detail="Tipo inválido de arquivo. Formato esperado: jpg")
    else:
        # ler o conteudo do post
        contents = await file.read()
        # criar um objeto BytesIO e escrever os dados da imagem nele.
        buffer = io.BytesIO(contents)
        imagem = Image.open(buffer)

        # cria uma pasta que vai conter a imagem recebida do front para ser usada pelo u2net
        nomePasta = uuid.uuid4()
        diretorioNovo = PASTA_IMAGENS_RECEBIDAS + os.sep + str(nomePasta)
        os.mkdir(diretorioNovo)
        caminhoDaImagem = diretorioNovo + os.sep + file.filename
        imagem = imagem.save(caminhoDaImagem)

        caminhoResultado = diretorioNovo + os.sep + 'result'
        os.mkdir(caminhoResultado)

        u2net.get_mask.makeMask(caminhoDaImagem, caminhoResultado)

        return {"filename": file.filename}


# @app.get("/items/{item_id}")
# async def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}


# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item):
#     return {"item_name": item.name, "item_id": item_id}