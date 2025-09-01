from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.ml_model import ModeleIA
from app.schemas.ml_model import MLModelCreate, MLModelUpdate, MLModelOut

router = APIRouter()

@router.post("/", response_model=MLModelOut, status_code=201)
def create_model(data: MLModelCreate, db: Session = Depends(get_db)):
    obj = ModeleIA(**data.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@router.get("/", response_model=list[MLModelOut])
def list_models(db: Session = Depends(get_db), sport_id: int | None = None, statut: str | None = None, limit: int = Query(100, le=500)):
    q = db.query(ModeleIA)
    if sport_id: q = q.filter(ModeleIA.sport_id == sport_id)
    if statut: q = q.filter(ModeleIA.statut == statut)
    return q.order_by(ModeleIA.created_at.desc()).limit(limit).all()

@router.get("/{model_id}", response_model=MLModelOut)
def get_model(model_id: int, db: Session = Depends(get_db)):
    obj = db.get(ModeleIA, model_id)
    if not obj: raise HTTPException(status_code=404, detail="Modèle introuvable")
    return obj

@router.patch("/{model_id}", response_model=MLModelOut)
def update_model(model_id: int, data: MLModelUpdate, db: Session = Depends(get_db)):
    obj = db.get(ModeleIA, model_id)
    if not obj: raise HTTPException(status_code=404, detail="Modèle introuvable")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit(); db.refresh(obj)
    return obj

@router.delete("/{model_id}", status_code=204)
def delete_model(model_id: int, db: Session = Depends(get_db)):
    obj = db.get(ModeleIA, model_id)
    if not obj: return
    db.delete(obj); db.commit()
