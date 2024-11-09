# app/routers/menus.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db

router = APIRouter()

@router.get("/", response_model=list[schemas.Menu])
def read_menu(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    menu = db.query(models.Menu).offset(skip).limit(limit).all()
    return menu

@router.get("/{plat_id}", response_model=schemas.Menu)
def get_menu_item_by_id(plat_id: int, db: Session = Depends(get_db)):
    menu_item = db.query(models.Menu).filter(models.Menu.plat_id == plat_id).first()
    if menu_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found")
    return menu_item

@router.post("/", response_model=schemas.Menu)
def create_menu_item(menu_item: schemas.MenuCreate, db: Session = Depends(get_db)):
    db_menu_item = models.Menu(**menu_item.dict())
    db.add(db_menu_item)
    db.commit()
    db.refresh(db_menu_item)
    return db_menu_item

@router.put("/{plat_id}", response_model=schemas.Menu)
def update_menu_item(plat_id: int, menu_item: schemas.MenuCreate, db: Session = Depends(get_db)):
    db_menu_item = db.query(models.Menu).filter(models.Menu.plat_id == plat_id).first()
    if db_menu_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found")
    for key, value in menu_item.dict().items():
        setattr(db_menu_item, key, value)
    db.commit()
    db.refresh(db_menu_item)
    return db_menu_item

@router.delete("/{plat_id}", response_model=dict)
def delete_menu_item(plat_id: int, db: Session = Depends(get_db)):
    db_menu_item = db.query(models.Menu).filter(models.Menu.plat_id == plat_id).first()
    if db_menu_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found")
    db.delete(db_menu_item)
    db.commit()
    return {"detail": "Menu item deleted successfully"}
