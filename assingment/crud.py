from sqlalchemy.orm import Session
from models import Item
from schemas import ItemCreate, ItemUpdate

def get_item(db: Session, item_id: int) -> Item:
    """
    Retrieve an item by its ID.
    
    :param db: Database session.
    :param item_id: ID of the item to retrieve.
    :return: Item object or None if not found.
    """
    return db.query(Item).filter(Item.id == item_id).first()

def get_items(db: Session, skip: int = 0, limit: int = 100) -> list[Item]:
    """
    Retrieve all items with pagination.
    
    :param db: Database session.
    :param skip: Number of records to skip.
    :param limit: Maximum number of records to return.
    :return: List of items.
    """
    return db.query(Item).offset(skip).limit(limit).all()

def create_item(db: Session, item: ItemCreate) -> Item:
    """
    Create a new item.
    
    :param db: Database session.
    :param item: Item data to create.
    :return: Created item object.
    """
    db_item = Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_item(db: Session, item_id: int, item: ItemUpdate) -> Item:
    """
    Update an existing item by its ID.
    
    :param db: Database session.
    :param item_id: ID of the item to update.
    :param item: Updated item data.
    :return: Updated item object or None if not found.
    """
    db_item = get_item(db, item_id)
    if db_item is None:
        return None
    for key, value in item.dict().items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_item(db: Session, item_id: int) -> Item:
    """
    Delete an item by its ID.
    
    :param db: Database session.
    :param item_id: ID of the item to delete.
    :return: Deleted item object or None if not found.
    """
    db_item = get_item(db, item_id)
    if db_item is None:
        return None
    db.delete(db_item)
    db.commit()
    return db_item

def search_items(db: Session, name: str = None, description: str = None, min_price: float = None, max_price: float = None, quantity: int = None) -> list[Item]:
    """
    Search for items based on various criteria.
    
    :param db: Database session.
    :param name: Name of the item (partial match).
    :param description: Description of the item (partial match).
    :param min_price: Minimum price of the item.
    :param max_price: Maximum price of the item.
    :param quantity: Quantity of the item (exact match).
    :return: List of items matching the criteria.
    """
    query = db.query(Item)
    if name:
        query = query.filter(Item.name.contains(name))
    if description:
        query = query.filter(Item.description.contains(description))
    if min_price is not None:
        query = query.filter(Item.price >= min_price)
    if max_price is not None:
        query = query.filter(Item.price <= max_price)
    if quantity is not None:
        query = query.filter(Item.quantity == quantity)
    return query.all()
