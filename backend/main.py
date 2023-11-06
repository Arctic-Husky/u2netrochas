from typing import Union

from fastapi import FastAPI, UploadFile
from pydantic import BaseModel

import json
# import uuid

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
    data = json.load(file.file.read())
    return {"filename": file.filename}


# @app.get("/items/{item_id}")
# async def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}


# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item):
#     return {"item_name": item.name, "item_id": item_id}