# Projet Restaurant - Test Bdd Mock

## Description

Ce projet est une API RESTful développée en Python avec FastAPI et SQLAlchemy. Elle est conçue pour gérer les opérations d'un restaurant en permettant d'interagir avec une base de données SQLite. L'API supporte les opérations CRUD (Create, Read, Update, Delete) pour diverses entités telles que les clients, les employés, les tables, le menu, les commandes et les réservations.

### Fonctionnalités principales

- Gestion complète des clients, employés, tables, menus, réservations et commandes.
- Utilisation de FastAPI pour une structure de projet claire et une documentation automatique.
- Intégration de SQLAlchemy pour la gestion de la base de données SQLite.
- Tests unitaires possibles pour chaque route (à implémenter) en utilisant pytest.

## Prérequis

Assurez-vous d'avoir **Python 3.8+** installé sur votre machine.

## Installation

Clonez le dépôt, puis installez les dépendances nécessaires en utilisant :

```bash
pip install -r requirements.txt
```

## Lancer le projet

Lancer le jeu en exécutant la commande suivante :

```bash
uvicorn app.main:app --reload --port 3000
```

L'API sera accessible par défaut à l'adresse http://localhost:3000.

## Tests

Les tests sont à effectuer dans les fichiers du dossier `tests`.

### Exécution des tests

- Utilisez la fonction `assert` pour vérifier les réponses et le comportement de l’API.

Pour lancer les tests, utilisez la commande suivante :

```bash
pytest
```
