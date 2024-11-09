# app/main.py
from fastapi import FastAPI
from app.routers import clients, employes, tables, reservations, menus, commandes, commande_details

app = FastAPI()

# Inclure les routes
app.include_router(clients.router, prefix="/api/clients", tags=["clients"])
app.include_router(employes.router, prefix="/api/employes", tags=["employes"])
app.include_router(tables.router, prefix="/api/tables", tags=["tables"])
app.include_router(reservations.router, prefix="/api/reservations", tags=["reservations"])
app.include_router(menus.router, prefix="/api/menus", tags=["menu"])
app.include_router(commandes.router, prefix="/api/commandes", tags=["commandes"])
app.include_router(commande_details.router, prefix="/api/commande_details", tags=["commande_details"])
