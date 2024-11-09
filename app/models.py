# app/models.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, Time
from sqlalchemy.orm import relationship
from app.database import Base

class Client(Base):
    __tablename__ = "Clients"
    client_id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, nullable=False)
    prenom = Column(String, nullable=False)
    telephone = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True)

class Employe(Base):
    __tablename__ = "Employes"
    employe_id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, nullable=False)
    prenom = Column(String, nullable=False)
    poste = Column(String, nullable=False)
    salaire = Column(Float, nullable=False)
    date_embauche = Column(Date, nullable=False)

class Table(Base):
    __tablename__ = "Tables"
    table_id = Column(Integer, primary_key=True, index=True)
    numero_table = Column(Integer, unique=True, nullable=False)
    capacite = Column(Integer, nullable=False)
    emplacement = Column(String)

class Reservation(Base):
    __tablename__ = "Reservations"
    reservation_id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("Clients.client_id"), nullable=False)
    table_id = Column(Integer, ForeignKey("Tables.table_id"), nullable=False)
    date_reservation = Column(Date, nullable=False)
    heure_reservation = Column(Time, nullable=False)
    nombre_personnes = Column(Integer, nullable=False)

class Menu(Base):
    __tablename__ = "Menu"
    plat_id = Column(Integer, primary_key=True, index=True)
    nom_plat = Column(String, nullable=False)
    description = Column(String)
    prix = Column(Float, nullable=False)
    categorie = Column(String, nullable=False)

class Commande(Base):
    __tablename__ = "Commandes"
    commande_id = Column(Integer, primary_key=True, index=True)
    reservation_id = Column(Integer, ForeignKey("Reservations.reservation_id"))
    employe_id = Column(Integer, ForeignKey("Employes.employe_id"), nullable=False)
    date_commande = Column(Date, nullable=False)
    heure_commande = Column(Time, nullable=False)
    statut = Column(String, nullable=False)

class CommandeDetail(Base):
    __tablename__ = "Commande_Details"
    commande_detail_id = Column(Integer, primary_key=True, index=True)
    commande_id = Column(Integer, ForeignKey("Commandes.commande_id"), nullable=False)
    plat_id = Column(Integer, ForeignKey("Menu.plat_id"), nullable=False)
    quantite = Column(Integer, nullable=False)
