# app/schemas.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import date, time

# --- Client Schemas ---

class ClientBase(BaseModel):
    nom: str
    prenom: str
    telephone: str
    email: Optional[str] = None

class ClientCreate(ClientBase):
    pass

class Client(ClientBase):
    client_id: int

    class Config:
        orm_mode = True

# --- Employe Schemas ---

class EmployeBase(BaseModel):
    nom: str
    prenom: str
    poste: str
    salaire: float
    date_embauche: date

class EmployeCreate(EmployeBase):
    pass

class Employe(EmployeBase):
    employe_id: int

    class Config:
        orm_mode = True

# --- Table Schemas ---

class TableBase(BaseModel):
    numero_table: int
    capacite: int
    emplacement: Optional[str] = None

class TableCreate(TableBase):
    pass

class Table(TableBase):
    table_id: int

    class Config:
        orm_mode = True

# --- Reservation Schemas ---

class ReservationBase(BaseModel):
    client_id: int
    table_id: int
    date_reservation: date
    heure_reservation: time
    nombre_personnes: int

class ReservationCreate(ReservationBase):
    pass

class Reservation(ReservationBase):
    reservation_id: int

    class Config:
        orm_mode = True

# --- Menu Schemas ---

class MenuBase(BaseModel):
    nom_plat: str
    description: Optional[str] = None
    prix: float
    categorie: str

class MenuCreate(MenuBase):
    pass

class Menu(MenuBase):
    plat_id: int

    class Config:
        orm_mode = True

# --- Commande Schemas ---

class CommandeBase(BaseModel):
    reservation_id: Optional[int] = None
    employe_id: int
    date_commande: date
    heure_commande: time
    statut: str

class CommandeCreate(CommandeBase):
    pass

class Commande(CommandeBase):
    commande_id: int

    class Config:
        orm_mode = True

# --- CommandeDetail Schemas ---

class CommandeDetailBase(BaseModel):
    commande_id: int
    plat_id: int
    quantite: int

class CommandeDetailCreate(CommandeDetailBase):
    pass

class CommandeDetail(CommandeDetailBase):
    commande_detail_id: int

    class Config:
        orm_mode = True
