from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.db.session import get_db
from app.models.model_monitoring import ModelMonitoring
from app.schemas.model_monitoring import MonitoringCreate, MonitoringOut, MonitoringUpdate

router = APIRouter()

@router.post("/", response_model=MonitoringOut, status_code=201)
def upsert_monitoring(data: MonitoringCreate, db: Session = Depends(get_db)):
    obj = db.query(ModelMonitoring).filter(
        and_(ModelMonitoring.modele_id == data.modele_id, ModelMonitoring.date_evaluation == data.date_evaluation)
    ).first()
    if obj:
        for k, v in data.model_dump().items():
            setattr(obj, k, v)
        db.commit(); db.refresh(obj)
        return obj
    obj = ModelMonitoring(**data.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@router.get("/by_model", response_model=list[MonitoringOut])
def get_monitoring_by_model(modele_id: int, db: Session = Depends(get_db)):
    return db.query(ModelMonitoring).filter(ModelMonitoring.modele_id == modele_id).order_by(ModelMonitoring.date_evaluation.desc()).all()
