from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import sessionmaker, Session, declarative_base

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    description = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


Base.metadata.create_all(bind=engine)


class ItemBase(BaseModel):
    name: str = Field(default="", max_length=100, title="Name of the item")
    description: str = Field(
        default="", max_length=255, title="Description of the item"
    )


class ItemCreate(ItemBase):
    pass


class ItemUpdate(ItemBase):
    pass


class ItemRes(ItemBase):
    id: int = Field(default=None, title="ID of the item")
    created_at: datetime = Field(title="Creation timestamp")
    updated_at: datetime = Field(title="Last update timestamp")

    model_config = ConfigDict(from_attributes=True)


app = FastAPI(
    title="FastAPI CRUD Example",
    version="1.0.0",
    description="A simple CRUD API for Items using FastAPI and SQLAlchemy .",
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get(
    "/items",
    operation_id="get_items",
)
def read_items(db: Session = Depends(get_db)) -> list[ItemRes]:
    items = db.query(Item).order_by(Item.created_at.desc()).all()
    return items


@app.post("/items", operation_id="create_item")
def create_item(item: ItemCreate, db: Session = Depends(get_db)) -> ItemRes:
    db_item = Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@app.get("/items/{item_id}", operation_id="get_item")
def read_item(item_id: int, db: Session = Depends(get_db)) -> ItemRes:
    item = db.query(Item).filter(Item.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.put("/items/{item_id}", operation_id="update_item")
def update_item(
    item_id: int, item_update: ItemUpdate, db: Session = Depends(get_db)
) -> ItemRes:
    item = db.query(Item).filter(Item.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    item.name = item_update.name
    item.description = item_update.description
    db.commit()
    db.refresh(item)
    return item


@app.delete("/items/{item_id}", operation_id="delete_item")
def delete_item(item_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    item = db.query(Item).filter(Item.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(item)
    db.commit()
    return {"detail": "Item deleted"}
