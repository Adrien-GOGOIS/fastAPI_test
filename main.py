from typing import Union
from fastapi import FastAPI
from enum import Enum

from database import fake_items

items = fake_items.fake_items_db

app = FastAPI()


class Cats(str, Enum):
    shoshana = "shoshana"
    jacques = "jacques"
    florence = "florence"


# Route par default
@app.get("/")
def read_root():
    return {"Hello": "World"}


# Récupérer un paramètre et renvoyer un élément de l'Enum
@app.get("/cats/{cat_name}")
def read_cat_name(cat_name: Cats):
    if cat_name is Cats.shoshana:
        return {"name": Cats.shoshana, "Caractéristiques": "Peureuse"}
    if cat_name is Cats.jacques:
        return {"name": Cats.jacques, "Caractéristiques": "Vieux"}


# Récupération d'un chemin de fichier et lecture
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    with open(file_path, 'r', encoding='utf8') as file_to_read:
        return {
            "file_path": file_path,
            "contenu": file_to_read.readline()
        }


# Query parameters
@app.get("/items")
async def read_item(skip: int = 0, limit: int = 10):  # Valeur par défault de 0 à 10
    return items[skip: skip + limit]


# Paramètres optionnels
@app.get("/items/{item_id}")
async def get_item(item_id: int, color: str | None = None):  # Color est soit une string, soit nul si non déclaré
    actual_item = None
    for item in items:
        if item['id'] is item_id:
            actual_item = item
        if color and actual_item:
            if actual_item['color'] == color:
                return {
                    "item": actual_item,
                    "message": "Couleur disponible"
                }
            return f"Couleur non disponible pour l'objet {actual_item['item']}"
        return actual_item
