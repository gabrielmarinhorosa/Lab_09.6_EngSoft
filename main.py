from typing import Annotated

import uvicorn
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, StringConstraints

app = FastAPI(title="Lab 09 - Items API")

ItemName = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


class ItemInput(BaseModel):
    name: ItemName


class Item(BaseModel):
    id: int
    name: str


class ItemResponse(BaseModel):
    item: Item


class ItemListResponse(BaseModel):
    items: list[Item]


class DeleteResponse(BaseModel):
    result: bool


# Sample data
items = [Item(id=1, name="Item 1"), Item(id=2, name="Item 2")]
next_id = 3


def find_item(item_id: int) -> Item:
    item = next((item for item in items if item.id == item_id), None)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


# Home page
@app.get("/")
def home():
    return {"message": "Lab 09 - Items API", "items": "/items", "docs": "/docs"}


# Get all items
@app.get("/items", response_model=ItemListResponse)
def get_items():
    return {"items": items}


# Get a specific item
@app.get("/items/{item_id}", response_model=ItemResponse)
def get_item(item_id: int):
    return {"item": find_item(item_id)}


# Create a new item
@app.post("/items", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(data: ItemInput):
    global next_id
    new_item = Item(id=next_id, name=data.name)
    next_id += 1
    items.append(new_item)
    return {"item": new_item}


# Update an existing item
@app.put("/items/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, data: ItemInput):
    item = find_item(item_id)
    item.name = data.name
    return {"item": item}


# Delete an item
@app.delete("/items/{item_id}", response_model=DeleteResponse)
def delete_item(item_id: int):
    items.remove(find_item(item_id))
    return {"result": True}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
