from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from app.db.session import get_db
from app.models.h2h import HistoriqueConfrontation
from app.schemas.h2h import H2HCreate, H2HOut, H2HUpdate

router = APIRouter()

@router.post("/", response_model=H2HOut, status_code=201)
def create_h2h(data: H2HCreate, db: Session = Depends(get_db)):
    obj = HistoriqueConfrontation(**data.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@router.get("/", response_model=list[H2HOut])
def list_h2h(
    db: Session = Depends(get_db),
    equipe1_id: int | None = None,
    equipe2_id: int | None = None,
    limit: int = Query(50, le=200),
):
    q = db.query(HistoriqueConfrontation)
    if equipe1_id and equipe2_id:
        q = q.filter(
            or_(
                and_(HistoriqueConfrontation.equipe1_id == equipe1_id, HistoriqueConfrontation.equipe2_id == equipe2_id),
                and_(HistoriqueConfrontation.equipe1_id == equipe2_id, HistoriqueConfrontation.equipe2_id == equipe1_id),
            )
        )
    return q.order_by(HistoriqueConfrontation.date_match.desc()).limit(limit).all()

@router.patch("/{h2h_id}", response_model=H2HOut)
def update_h2h(h2h_id: int, data: H2HUpdate, db: Session = Depends(get_db)):
    obj = db.get(HistoriqueConfrontation, h2h_id)
    if not obj: raise HTTPException(status_code=404, detail="H2H introuvable")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit(); db.refresh(obj)
    return obj

@router.delete("/{h2h_id}", status_code=204)
def delete_h2h(h2h_id: int, db: Session = Depends(get_db)):
    obj = db.get(HistoriqueConfrontation, h2h_id)
    if not obj: return
    db.delete(obj); db.commit()
