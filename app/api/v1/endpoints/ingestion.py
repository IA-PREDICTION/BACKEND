from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

from app.db.session import get_db
from app.models.source_donnee import SourceDonnee
from app.models.log_ingestion import LogIngestion
from app.schemas.ingestion import (
    SourceDonneeCreate, SourceDonneeUpdate, SourceDonneeOut,
    LogIngestionCreate, LogIngestionOut
)

router = APIRouter()

# --- Sources ---

@router.post("/sources", response_model=SourceDonneeOut)
def create_source(payload: SourceDonneeCreate, db: Session = Depends(get_db)):
    src = SourceDonnee(**payload.model_dump())
    db.add(src)
    db.commit()
    db.refresh(src)
    return src

@router.get("/sources", response_model=List[SourceDonneeOut])
def list_sources(db: Session = Depends(get_db)):
    return db.query(SourceDonnee).order_by(SourceDonnee.id.desc()).all()

@router.get("/sources/{source_id}", response_model=SourceDonneeOut)
def get_source(source_id: int, db: Session = Depends(get_db)):
    src = db.get(SourceDonnee, source_id)
    if not src:
        raise HTTPException(404, "Source introuvable")
    return src

@router.patch("/sources/{source_id}", response_model=SourceDonneeOut)
def update_source(source_id: int, payload: SourceDonneeUpdate, db: Session = Depends(get_db)):
    src = db.get(SourceDonnee, source_id)
    if not src:
        raise HTTPException(404, "Source introuvable")
    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(src, k, v)
    db.add(src); db.commit(); db.refresh(src)
    return src

@router.post("/sources/{source_id}/schedule/next", response_model=SourceDonneeOut)
def schedule_next_run(source_id: int, minutes: int = Query(15, ge=1, le=10080), db: Session = Depends(get_db)):
    src = db.get(SourceDonnee, source_id)
    if not src:
        raise HTTPException(404, "Source introuvable")
    src.prochaine_synchro = datetime.utcnow() + timedelta(minutes=minutes)
    db.add(src); db.commit(); db.refresh(src)
    return src

# --- Logs ---

@router.post("/logs", response_model=LogIngestionOut)
def add_log(payload: LogIngestionCreate, db: Session = Depends(get_db)):
    # Vérifier source
    if not db.get(SourceDonnee, payload.source_id):
        raise HTTPException(400, "source_id invalide")
    log = LogIngestion(**payload.model_dump())
    db.add(log); db.commit(); db.refresh(log)
    return log

@router.get("/logs", response_model=List[LogIngestionOut])
def list_logs(source_id: Optional[int] = None, limit: int = 100, db: Session = Depends(get_db)):
    q = db.query(LogIngestion).order_by(LogIngestion.id.desc())
    if source_id:
        q = q.filter(LogIngestion.source_id == source_id)
    return q.limit(limit).all()
