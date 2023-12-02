from typing import Union
from fastapi import FastAPI, UploadFile, File, status
from fastapi.exceptions import HTTPException
from PIL import Image
from fastapi.responses import Response
from starlette.middleware.cors import CORSMiddleware
from secret_settings import *

from pydantic import BaseModel

class Busca(BaseModel):
    stringBusca: str

from supabase import create_client, Client

url: str = SUPABASE_URL
key: str = SUPABASE_KEY
supabase: Client = create_client(url, key)

import uuid
import io as pythonio
import os
import shutil
import base64

import sys
sys.path.append("E:\\Repositorios\\U-2-Net")
print(sys.path)
from u2net.u2net_test import *
from opencv.remove_background import *

PASTA_IMAGENS_RECEBIDAS = ".."+os.sep+"imagens_recebidas"

pastas_deletar = []

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# TODO: tratamento de imagem corrompida, imagem de texto que foi mudada de .txt para .jpg
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if file.content_type != "image/jpeg":
        raise HTTPException(400, detail="Tipo inválido de arquivo. Formato esperado: jpg")
    else:
        # ler o conteudo do post
        contents = await file.read()
        # criar um objeto BytesIO e escrever os dados da imagem nele.
        buffer = pythonio.BytesIO(contents)
        imagem = Image.open(buffer)

        # cria uma pasta que vai conter a imagem recebida do front para ser usada pelo u2net
        nomePasta = uuid.uuid4()
        diretorioNovo = PASTA_IMAGENS_RECEBIDAS + os.sep + str(nomePasta)
        os.mkdir(diretorioNovo)
        caminhoDaImagem = diretorioNovo + os.sep + file.filename
        try:
            imagem = imagem.save(caminhoDaImagem)

            caminhoMascara = diretorioNovo + os.sep + 'mask' + os.sep
            os.mkdir(caminhoMascara)

            makeMask(caminhoDaImagem, caminhoMascara)

            caminhoResultado = diretorioNovo + os.sep + 'result' + os.sep
            os.mkdir(caminhoResultado)

            caminhoImagens = diretorioNovo + os.sep

            imagemResultado = removeBackground(pastaImagens=caminhoImagens, pastaMascaras=caminhoMascara, pastaResultados=caminhoResultado, fileName=file.filename)

            with open(imagemResultado, "rb") as image_file:
                data = base64.b64encode(image_file.read())

            return Response(content=data, media_type="image/png")
        finally:
            deletarPasta(diretorioNovo)

@app.get("/catalogo")
async def get_catalogo(status_code=status.HTTP_200_OK):
    data, count = supabase.table('CHAPAS').select("*").order('DATA_CRIACAO', desc=True).execute()
    return data

@app.post("/busca")
async def get_catalogo_busca(busca: Busca, status_code=status.HTTP_200_OK):
    data, count = supabase.table('CHAPAS').select("*").ilike('NOME_ARQUIVO',busca.stringBusca).order('DATA_CRIACAO', desc=True).execute()
    return data


@app.post("/salvar")
async def salvar_imagem(file: UploadFile = File(...), status_code=status.HTTP_200_OK):
    # ler o conteudo do post
    contents = await file.read()

    nomeArquivo = uuid.uuid4()

    supabase.storage.from_("Imagens").upload(file=contents,path="{}".format(nomeArquivo),file_options={"content-type": "image/png"})

    res = supabase.storage.from_('Imagens').get_public_url('{}'.format(nomeArquivo))

    data, count = supabase.table('CHAPAS').insert({"NOME_ARQUIVO": file.filename, "URL_ARQUIVO": "{}".format(res)}).execute()

    return data
            
def deletarPasta(pasta: str):
    shutil.rmtree(pasta)