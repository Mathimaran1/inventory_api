from fastapi import FastAPI, HTTPException, Query
from pymongo import MongoClient
from pydantic import BaseModel
from dotenv import load_dotenv
from typing import Optional, List
import os

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("DB_NAME")]
col = db["items"]

app = FastAPI()

class Item(BaseModel):
    id: int
    name: str
    quantity: int
    category: str
    price: float
    available: bool

def stock_status(quantity):

    if quantity > 10:
        return "Good stock"

    elif quantity > 0:
        return "Low stock"

    else:
        return "Out of stock"


# -------------------------
# Create Item
# -------------------------

@app.post("/items")
def create_item(item: Item):

    # Check duplicate ID
    if col.find_one({"_id": item.id}):
        raise HTTPException(409, "Item ID already exists")

    data = item.model_dump()

    # Store id as _id
    data["_id"] = data.pop("id")

    col.insert_one(data)

    return {
        "message": "Item created"
    }


# @app.get("/items/{item_id}")
# def get_item(item_id: int):

#     item = col.find_one({"_id": item_id})

#     if not item:
#         raise HTTPException(404, "Item not found")

#     return {
#         "id": item["_id"],
#         "name": item["name"],
#         "category": item["category"],
#         "quantity": item["quantity"],
#         "price": item["price"],
#         "available": item["available"],
#         "stock_status": stock_status(item["quantity"])
#     }


@app.get("/items")
def filter_items(
    category: Optional[str] = Query(None),
    name: Optional[str] = Query(None),
    item_id: Optional[int] = Query(None)
):

    query = {}

    if category:
        query["category"] = category

    if name:
        query["name"] = name

    if item_id:
        query["_id"] = item_id

    items = []

    for item in col.find(query):

        items.append({
            "id": item["_id"],
            "name": item["name"],
            "category": item["category"],
            "quantity": item["quantity"],
            "price": item["price"],
            "available": item["available"],
            "stock_status": stock_status(item["quantity"])
        })

    if not items:
        raise HTTPException(404, "No items found")

    return items