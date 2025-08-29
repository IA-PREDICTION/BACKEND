# BACKEND

ia_pronostic/
│
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── endpoints/
│   │   │   │   ├── auth.py
│   │   │   │   ├── users.py
│   │   │   │   ├── matches.py
│   │   │   │   └── predictions.py
│   │   │   └── __init__.py
│   │   └── __init__.py
│   │
│   ├── core/
│   │   ├── config.py         # Paramètres globaux (env, secrets)
│   │   ├── security.py       # Gestion JWT, OAuth, 2FA
│   │   └── utils.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── match.py
│   │   ├── prediction.py
│   │   └── base.py
│   │
│   ├── schemas/
│   │   ├── user.py
│   │   ├── auth.py
│   │   ├── match.py
│   │   └── prediction.py
│   │
│   ├── services/
│   │   ├── user_service.py
│   │   ├── prediction_service.py
│   │   └── match_service.py
│   │
│   ├── db/
│   │   ├── session.py        # Connexion DB SQLAlchemy
│   │   ├── base_class.py     # Pour déclarer Base = declarative_base()
│   │   └── init_db.py        # Insertion de données initiales
│   │
│   └── main.py               # Point d'entrée FastAPI
│
├── alembic/                  # Migrations de base de données
│
├── .env                      # Variables d'environnement
├── requirements.txt
└── README.md
