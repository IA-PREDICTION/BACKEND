from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.db.session import get_db
from app.models.features_engineering import FeaturesEngineering
from app.schemas.features_engineering import FeaturesEngCreate, FeaturesEngOut, FeaturesEngUpdate

router = APIRouter()

@router.post("/", response_model=FeaturesEngOut, status_code=201)
def upsert_features(data: FeaturesEngCreate, db: Session = Depends(get_db)):
    obj = db.query(FeaturesEngineering).filter(
        and_(FeaturesEngineering.match_id == data.match_id, FeaturesEngineering.modele_id == data.modele_id)
    ).first()
    if obj:
        for k, v in data.model_dump().items():
            setattr(obj, k, v)
        db.commit(); db.refresh(obj)
        return obj
    obj = FeaturesEngineering(**data.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@router.get("/by_match_model", response_model=FeaturesEngOut)
def get_features(match_id: int, modele_id: int, db: Session = Depends(get_db)):
    obj = db.query(FeaturesEngineering).filter(
        and_(FeaturesEngineering.match_id == match_id, FeaturesEngineering.modele_id == modele_id)
    ).first()
    if not obj: raise HTTPException(status_code=404, detail="Features introuvables")
    return obj
