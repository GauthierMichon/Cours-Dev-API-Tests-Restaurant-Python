# app/routers/commande_details.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db

router = APIRouter()

@router.get("/", response_model=list[schemas.CommandeDetail])
def read_commande_details(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    commande_details = db.query(models.CommandeDetail).offset(skip).limit(limit).all()
    return commande_details

@router.get("/{commande_detail_id}", response_model=schemas.CommandeDetail)
def get_commande_detail_by_id(commande_detail_id: int, db: Session = Depends(get_db)):
    commande_detail = db.query(models.CommandeDetail).filter(models.CommandeDetail.commande_detail_id == commande_detail_id).first()
    if commande_detail is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Commande Detail not found")
    return commande_detail

@router.post("/", response_model=schemas.CommandeDetail)
def create_commande_detail(commande_detail: schemas.CommandeDetailCreate, db: Session = Depends(get_db)):
    db_commande_detail = models.CommandeDetail(**commande_detail.dict())
    db.add(db_commande_detail)
    db.commit()
    db.refresh(db_commande_detail)
    return db_commande_detail

@router.put("/{commande_detail_id}", response_model=schemas.CommandeDetail)
def update_commande_detail(commande_detail_id: int, commande_detail: schemas.CommandeDetailCreate, db: Session = Depends(get_db)):
    db_commande_detail = db.query(models.CommandeDetail).filter(models.CommandeDetail.commande_detail_id == commande_detail_id).first()
    if db_commande_detail is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Commande Detail not found")
    for key, value in commande_detail.dict().items():
        setattr(db_commande_detail, key, value)
    db.commit()
    db.refresh(db_commande_detail)
    return db_commande_detail

@router.delete("/{commande_detail_id}", response_model=dict)
def delete_commande_detail(commande_detail_id: int, db: Session = Depends(get_db)):
    db_commande_detail = db.query(models.CommandeDetail).filter(models.CommandeDetail.commande_detail_id == commande_detail_id).first()
    if db_commande_detail is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Commande Detail not found")
    db.delete(db_commande_detail)
    db.commit()
    return {"detail": "Commande Detail deleted successfully"}
