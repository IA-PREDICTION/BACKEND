from fastapi import FastAPI
from app.api.v1.endpoints import auth, users, matches, predictions
from app.db.init_db import init_db

app = FastAPI(title="IA Pronostic")

init_db()  # Crée les tables au démarrage une fois

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(matches.router, prefix="/api/v1/matches", tags=["matches"])
app.include_router(predictions.router, prefix="/api/v1/predictions", tags=["predictions"])
