from fastapi import FastAPI
from app.api.v1.endpoints import auth, sports, leagues, teams, matches, odds, stats, h2h, players, injuries

# from app.db.session import engine
# from app.models.base import Base

app = FastAPI(title="IA Pronostic")

# Routes
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(sports.router,  prefix="/api/v1/sports",  tags=["sports"])
app.include_router(leagues.router, prefix="/api/v1/leagues", tags=["leagues"])
app.include_router(teams.router,   prefix="/api/v1/teams",   tags=["teams"])
app.include_router(matches.router, prefix="/api/v1/matches", tags=["matches"])

app.include_router(odds.router,    prefix="/api/v1/odds",     tags=["odds"])
app.include_router(stats.router,   prefix="/api/v1/stats",    tags=["stats"])
app.include_router(h2h.router,     prefix="/api/v1/h2h",      tags=["h2h"])
app.include_router(players.router, prefix="/api/v1/players",  tags=["players"])
app.include_router(injuries.router,prefix="/api/v1/injuries", tags=["injuries"])