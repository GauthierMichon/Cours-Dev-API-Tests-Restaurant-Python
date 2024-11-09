# app/routers/commandes.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db

router = APIRouter()

@router.get("/", response_model=list[schemas.Commande])
def read_commandes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    commandes = db.query(models.Commande).offset(skip).limit(limit).all()
    return commandes

@router.get("/{commande_id}", response_model=schemas.Commande)
def get_commande_by_id(commande_id: int, db: Session = Depends(get_db)):
    commande = db.query(models.Commande).filter(models.Commande.commande_id == commande_id).first()
    if commande is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Commande not found")
    return commande

@router.post("/", response_model=schemas.Commande)
def create_commande(commande: schemas.CommandeCreate, db: Session = Depends(get_db)):
    db_commande = models.Commande(**commande.dict())
    db.add(db_commande)
    db.commit()
    db.refresh(db_commande)
    return db_commande

@router.put("/{commande_id}", response_model=schemas.Commande)
def update_commande(commande_id: int, commande: schemas.CommandeCreate, db: Session = Depends(get_db)):
    db_commande = db.query(models.Commande).filter(models.Commande.commande_id == commande_id).first()
    if db_commande is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Commande not found")
    for key, value in commande.dict().items():
        setattr(db_commande, key, value)
    db.commit()
    db.refresh(db_commande)
    return db_commande

@router.delete("/{commande_id}", response_model=dict)
def delete_commande(commande_id: int, db: Session = Depends(get_db)):
    db_commande = db.query(models.Commande).filter(models.Commande.commande_id == commande_id).first()
    if db_commande is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Commande not found")
    db.delete(db_commande)
    db.commit()
    return {"detail": "Commande deleted successfully"}
