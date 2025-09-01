from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.db.session import get_db
from app.models.blessure import BlessureSuspension
from app.schemas.blessure import BlessureCreate, BlessureOut, BlessureUpdate

router = APIRouter()

@router.post("/", response_model=BlessureOut, status_code=201)
def create_injury(data: BlessureCreate, db: Session = Depends(get_db)):
    obj = BlessureSuspension(**data.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@router.get("/", response_model=list[BlessureOut])
def list_injuries(
    db: Session = Depends(get_db),
    equipe_id: int | None = None,
    joueur_id: int | None = None,
    type: str | None = None,
    limit: int = Query(100, le=500),
):
    q = db.query(BlessureSuspension)
    if equipe_id: q = q.filter(BlessureSuspension.equipe_id == equipe_id)
    if joueur_id: q = q.filter(BlessureSuspension.joueur_id == joueur_id)
    if type: q = q.filter(BlessureSuspension.type == type)
    return q.order_by(BlessureSuspension.created_at.desc()).limit(limit).all()

@router.patch("/{indispo_id}", response_model=BlessureOut)
def update_injury(indispo_id: int, data: BlessureUpdate, db: Session = Depends(get_db)):
    obj = db.get(BlessureSuspension, indispo_id)
    if not obj: raise HTTPException(status_code=404, detail="Enregistrement introuvable")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit(); db.refresh(obj)
    return obj

@router.delete("/{indispo_id}", status_code=204)
def delete_injury(indispo_id: int, db: Session = Depends(get_db)):
    obj = db.get(BlessureSuspension, indispo_id)
    if not obj: return
    db.delete(obj); db.commit()
