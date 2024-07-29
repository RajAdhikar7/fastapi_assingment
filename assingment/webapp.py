from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from database import SessionLocal, engine
import models
import schemas
import crud

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/items/", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    """
    Create a new item.
    
    :param item: Item data to create.
    :param db: Database session.
    :return: Created item object.
    """
    return crud.create_item(db=db, item=item)

@app.get("/items/", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Retrieve all items with pagination.
    
    :param skip: Number of records to skip.
    :param limit: Maximum number of records to return.
    :param db: Database session.
    :return: List of items.
    """
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

@app.get("/items/{item_id}", response_model=schemas.Item)
def read_item(item_id: int, db: Session = Depends(get_db)):
    """
    Retrieve an item by its ID.
    
    :param item_id: ID of the item to retrieve.
    :param db: Database session.
    :return: Item object or 404 error if not found.
    """
    db_item = crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.put("/items/{item_id}", response_model=schemas.Item)
def update_item(item_id: int, item: schemas.ItemUpdate, db: Session = Depends(get_db)):
    """
    Update an existing item by its ID.
    
    :param item_id: ID of the item to update.
    :param item: Updated item data.
    :param db: Database session.
    :return: Updated item object or 404 error if not found.
    """
    db_item = crud.update_item(db, item_id=item_id, item=item)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.delete("/items/{item_id}", response_model=schemas.Item)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    """
    Delete an item by its ID.
    
    :param item_id: ID of the item to delete.
    :param db: Database session.
    :return: Deleted item object or 404 error if not found.
    """
    db_item = crud.delete_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.get("/items/search/", response_model=List[schemas.Item])
def search_items(
    name: Optional[str] = None,
    description: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    quantity: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Search for items based on various criteria.
    
    :param name: Name of the item (partial match).
    :param description: Description of the item (partial match).
    :param min_price: Minimum price of the item.
    :param max_price: Maximum price of the item.
    :param quantity: Quantity of the item (exact match).
    :param db: Database session.
    :return: List of items matching the criteria.
    """
    items = crud.search_items(db, name=name, description=description, min_price=min_price, max_price=max_price, quantity=quantity)
    return items
