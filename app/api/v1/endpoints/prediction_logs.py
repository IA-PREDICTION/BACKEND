from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.prediction_log import LogPrediction
from app.schemas.prediction_log import PredLogCreate, PredLogOut

router = APIRouter()

@router.post("/", response_model=PredLogOut, status_code=201)
def create_log(data: PredLogCreate, db: Session = Depends(get_db)):
    obj = LogPrediction(**data.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@router.get("/", response_model=list[PredLogOut])
def list_logs(db: Session = Depends(get_db), modele_id: int | None = None, limit: int = Query(200, le=1000)):
    q = db.query(LogPrediction)
    if modele_id: q = q.filter(LogPrediction.modele_id == modele_id)
    return q.order_by(LogPrediction.created_at.desc()).limit(limit).all()
