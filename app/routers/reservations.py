# app/routers/reservations.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db

router = APIRouter()

@router.get("/", response_model=list[schemas.Reservation])
def read_reservations(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    reservations = db.query(models.Reservation).offset(skip).limit(limit).all()
    return reservations

@router.get("/{reservation_id}", response_model=schemas.Reservation)
def get_reservation_by_id(reservation_id: int, db: Session = Depends(get_db)):
    reservation = db.query(models.Reservation).filter(models.Reservation.reservation_id == reservation_id).first()
    if reservation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reservation not found")
    return reservation

@router.post("/", response_model=schemas.Reservation)
def create_reservation(reservation: schemas.ReservationCreate, db: Session = Depends(get_db)):
    db_reservation = models.Reservation(**reservation.dict())
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation

@router.put("/{reservation_id}", response_model=schemas.Reservation)
def update_reservation(reservation_id: int, reservation: schemas.ReservationCreate, db: Session = Depends(get_db)):
    db_reservation = db.query(models.Reservation).filter(models.Reservation.reservation_id == reservation_id).first()
    if db_reservation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reservation not found")
    for key, value in reservation.dict().items():
        setattr(db_reservation, key, value)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation

@router.delete("/{reservation_id}", response_model=dict)
def delete_reservation(reservation_id: int, db: Session = Depends(get_db)):
    db_reservation = db.query(models.Reservation).filter(models.Reservation.reservation_id == reservation_id).first()
    if db_reservation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reservation not found")
    db.delete(db_reservation)
    db.commit()
    return {"detail": "Reservation deleted successfully"}
