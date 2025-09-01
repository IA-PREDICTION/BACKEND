from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.db.session import get_db
from app.models.prediction import Prediction
from app.schemas.prediction import PredictionCreate, PredictionOut, PredictionUpdate

router = APIRouter()

@router.post("/", response_model=PredictionOut, status_code=201)
def create_prediction(data: PredictionCreate, db: Session = Depends(get_db)):
    obj = Prediction(**data.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@router.get("/", response_model=list[PredictionOut])
def list_predictions(
    db: Session = Depends(get_db),
    match_id: int | None = None,
    modele_id: int | None = None,
    limit: int = Query(200, le=1000),
):
    q = db.query(Prediction)
    if match_id: q = q.filter(Prediction.match_id == match_id)
    if modele_id: q = q.filter(Prediction.modele_id == modele_id)
    return q.order_by(Prediction.date_prediction.desc()).limit(limit).all()

@router.patch("/{prediction_id}", response_model=PredictionOut)
def update_prediction(prediction_id: int, data: PredictionUpdate, db: Session = Depends(get_db)):
    obj = db.get(Prediction, prediction_id)
    if not obj: raise HTTPException(status_code=404, detail="Prédiction introuvable")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit(); db.refresh(obj)
    return obj

@router.delete("/{prediction_id}", status_code=204)
def delete_prediction(prediction_id: int, db: Session = Depends(get_db)):
    obj = db.get(Prediction, prediction_id)
    if not obj: return
    db.delete(obj); db.commit()
