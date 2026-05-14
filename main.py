from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"), tlsAllowInvalidCertificates=True, tlsAllowInvalidHostnames=True)
col = client[os.getenv("DB_NAME")]["items"]

app = FastAPI()

class Item(BaseModel):
    id: int
    name: str
    quantity: int
    category: str

def to_item(doc):
    return Item(id=doc["_id"], name=doc["name"], quantity=doc["quantity"], category=doc["category"])

@app.post("/items", status_code=201)
def create_item(item: Item):
    if col.find_one({"_id": item.id}):
        raise HTTPException(409, f"ID '{item.id}' already exists")
    if col.find_one({"name": item.name}):
        raise HTTPException(409, f"Name '{item.name}' already exists")
    d = item.model_dump()
    d["_id"] = d.pop("id")
    col.insert_one(d)
    return {"message": "Item created", "item": to_item(col.find_one({"_id": item.id}))}

@app.get("/items/id/{item_id}", response_model=Item)
def get_by_id(item_id: int):
    doc = col.find_one({"_id": item_id})
    if not doc:
        raise HTTPException(404, f"ID '{item_id}' not found")
    return to_item(doc)

@app.get("/items/name/{name}", response_model=Item)
def get_by_name(name: str):
    doc = col.find_one({"name": name})
    if not doc:
        raise HTTPException(404, f"Name '{name}' not found")
    return to_item(doc)
