# app/routers/tables.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db

router = APIRouter()

@router.get("/", response_model=list[schemas.Table])
def read_tables(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    tables = db.query(models.Table).offset(skip).limit(limit).all()
    return tables

@router.get("/{table_id}", response_model=schemas.Table)
def get_table_by_id(table_id: int, db: Session = Depends(get_db)):
    table = db.query(models.Table).filter(models.Table.table_id == table_id).first()
    if table is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Table not found")
    return table

@router.post("/", response_model=schemas.Table)
def create_table(table: schemas.TableCreate, db: Session = Depends(get_db)):
    db_table = models.Table(**table.dict())
    db.add(db_table)
    db.commit()
    db.refresh(db_table)
    return db_table

@router.put("/{table_id}", response_model=schemas.Table)
def update_table(table_id: int, table: schemas.TableCreate, db: Session = Depends(get_db)):
    db_table = db.query(models.Table).filter(models.Table.table_id == table_id).first()
    if db_table is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Table not found")
    for key, value in table.dict().items():
        setattr(db_table, key, value)
    db.commit()
    db.refresh(db_table)
    return db_table

@router.delete("/{table_id}", response_model=dict)
def delete_table(table_id: int, db: Session = Depends(get_db)):
    db_table = db.query(models.Table).filter(models.Table.table_id == table_id).first()
    if db_table is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Table not found")
    db.delete(db_table)
    db.commit()
    return {"detail": "Table deleted successfully"}
