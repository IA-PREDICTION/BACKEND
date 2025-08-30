from fastapi import FastAPI
from app.api.v1.endpoints import auth  # ajoute users/matches/predictions seulement s'ils existent et exposent `router`
from app.db.session import engine
from app.models.base import Base

app = FastAPI(title="IA Pronostic")

# Routes
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])

