import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, close_all_sessions
from app.main import app
from app.database import get_db, Base
from datetime import datetime
import random
import tempfile

# Créer un fichier temporaire pour SQLite
temp_db_file = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{temp_db_file.name}"

# Configuration du moteur et de la session
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override de la dépendance get_db pour utiliser la base de données temporaire
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Application de l'override pour tous les tests
app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

# Fixture pour configurer et nettoyer la base de données
@pytest.fixture(scope="module", autouse=True)
def setup_database():
    # Crée les tables avant les tests
    Base.metadata.create_all(bind=engine)
    yield
    # Ferme toutes les sessions et le moteur avant de supprimer le fichier
    close_all_sessions()
    engine.dispose()  # Ferme toutes les connexions au moteur
    temp_db_file.close()  # Ferme le fichier temporaire
    os.remove(temp_db_file.name)  # Supprime le fichier temporaire

# Fixture pour ajouter un client de test
@pytest.fixture
def client_data():
    # Génère un numéro de téléphone et un email uniques
    random_phone = f"{random.randint(1000000000, 9999999999)}"
    unique_email = f"johndoe_{datetime.now().timestamp()}@example.com"
    
    response = client.post("/api/clients/", json={
        "nom": "Doe",
        "prenom": "John",
        "telephone": random_phone,
        "email": unique_email
    })
    assert response.status_code == 200
    return response.json()

# Tests CRUD pour le client
def test_get_client_by_id(client_data):
    response = client.get(f"/api/clients/{client_data['client_id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["client_id"] == client_data["client_id"]
    assert data["nom"] == "Doe"

def test_update_client(client_data):
    response = client.put(f"/api/clients/{client_data['client_id']}", json={
        "nom": "Doe",
        "prenom": "Jane",
        "telephone": client_data["telephone"],
        "email": client_data["email"]
    })
    assert response.status_code == 200
    data = response.json()
    assert data["prenom"] == "Jane"
    assert data["email"] == client_data["email"]

def test_delete_client(client_data):
    response = client.delete(f"/api/clients/{client_data['client_id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["detail"] == "Client deleted successfully"
    # Vérifie que le client n'existe plus
    response = client.get(f"/api/clients/{client_data['client_id']}")
    assert response.status_code == 404
