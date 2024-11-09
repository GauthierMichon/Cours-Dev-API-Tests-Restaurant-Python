# app/routers/employes.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db

router = APIRouter()

@router.get("/", response_model=list[schemas.Employe])
def read_employes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    employes = db.query(models.Employe).offset(skip).limit(limit).all()
    return employes

@router.get("/{employe_id}", response_model=schemas.Employe)
def get_employe_by_id(employe_id: int, db: Session = Depends(get_db)):
    employe = db.query(models.Employe).filter(models.Employe.employe_id == employe_id).first()
    if employe is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employe not found")
    return employe

@router.post("/", response_model=schemas.Employe)
def create_employe(employe: schemas.EmployeCreate, db: Session = Depends(get_db)):
    db_employe = models.Employe(**employe.dict())
    db.add(db_employe)
    db.commit()
    db.refresh(db_employe)
    return db_employe

@router.put("/{employe_id}", response_model=schemas.Employe)
def update_employe(employe_id: int, employe: schemas.EmployeCreate, db: Session = Depends(get_db)):
    db_employe = db.query(models.Employe).filter(models.Employe.employe_id == employe_id).first()
    if db_employe is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employe not found")
    for key, value in employe.dict().items():
        setattr(db_employe, key, value)
    db.commit()
    db.refresh(db_employe)
    return db_employe

@router.delete("/{employe_id}", response_model=dict)
def delete_employe(employe_id: int, db: Session = Depends(get_db)):
    db_employe = db.query(models.Employe).filter(models.Employe.employe_id == employe_id).first()
    if db_employe is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employe not found")
    db.delete(db_employe)
    db.commit()
    return {"detail": "Employe deleted successfully"}
