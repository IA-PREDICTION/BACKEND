from fastapi import FastAPI
from app.api.v1.endpoints import (
    auth, ml_predict, sports, leagues, teams, matches, odds, stats, h2h, players, injuries,
    ml_models, feature_store, features_eng, predictions as ia_predictions, prediction_logs, monitoring
)

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

app.include_router(ml_models.router,      prefix="/api/v1/ml/models",      tags=["ml-models"])
app.include_router(feature_store.router,  prefix="/api/v1/ml/features",    tags=["feature-store"])
app.include_router(features_eng.router,   prefix="/api/v1/ml/engineering", tags=["features-eng"])
app.include_router(ia_predictions.router, prefix="/api/v1/ml/predictions", tags=["predictions"])
app.include_router(prediction_logs.router,prefix="/api/v1/ml/logs",        tags=["prediction-logs"])
app.include_router(monitoring.router,     prefix="/api/v1/ml/monitoring",  tags=["monitoring"])

app.include_router(ml_predict.router, prefix="/api/v1/ml/predict", tags=["predict"])