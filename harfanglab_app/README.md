# Videogame API

API REST Django pour gérer une base de données de jeux vidéo et plateformes.

## Installation rapide

```bash
# Cloner le projet
git clone <url-du-repo>
cd videogame-api

# Installer les dépendances avec uv
uv sync

# Migrations
uv run python manage.py migrate

# Créer un superuser pour l'admin
uv run python manage.py createsuperuser

# Charger les données d'exemple
uv run python manage.py load_sample_data

# Lancer le serveur
uv run python manage.py runserver
```

## Endpoints disponibles

### Jeux
- `GET /api/games/` - Liste des jeux
- `POST /api/games/` - Créer un jeu
- `GET /api/games/{id}/` - Détails d'un jeu
- `PUT /api/games/{id}/` - Modifier un jeu
- `DELETE /api/games/{id}/` - Supprimer un jeu

### Actions spéciales
- `GET /api/games/by_studio/?studio=Nintendo` - Jeux par studio
- `GET /api/games/by_platform/?platform=Switch` - Jeux par plateforme
- `GET /api/games/top_rated/?min_rating=15` - Jeux bien notés

### Plateformes
- `GET /api/platforms/` - Liste des plateformes
- `POST /api/platforms/` - Créer une plateforme

## Documentation API (Swagger très peu complet)

- **Swagger UI** : http://localhost:8000/api/docs/
- **Admin Django** : http://localhost:8000/admin/

## Exemple de test

```bash
# Créer une plateforme
curl -X POST http://localhost:8000/api/platforms/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Steam Deck"}'

# Créer un jeu
curl -X POST http://localhost:8000/api/games/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Elden Ring",
    "release_date": "2022-02-25",
    "studio": "FromSoftware",
    "ratings": 18,
    "platforms": ["PC", "PS5"]
  }'

# Lister les jeux
curl http://localhost:8000/api/games/
```

## Technologies utilisées

- **Django 5.0**
- **Django REST Framework**
- **django-filter** - Filtres
- **drf-spectacular** - Documentation OpenAPI
- **uv** - Gestionnaire de dépendances
- **SQLite** - Base de données
