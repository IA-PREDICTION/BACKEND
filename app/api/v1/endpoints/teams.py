from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.equipe import Equipe
from app.schemas.equipe import EquipeCreate, EquipeOut, EquipeUpdate

router = APIRouter()

@router.post("/", response_model=EquipeOut, status_code=201)
def create_team(data: EquipeCreate, db: Session = Depends(get_db)):
    obj = Equipe(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("/", response_model=list[EquipeOut])
def list_teams(db: Session = Depends(get_db), skip: int = 0, limit: int = Query(50, le=100), sport_id: int | None = None):
    q = db.query(Equipe)
    if sport_id:
        q = q.filter(Equipe.sport_id == sport_id)
    return q.offset(skip).limit(limit).all()

@router.get("/{team_id}", response_model=EquipeOut)
def get_team(team_id: int, db: Session = Depends(get_db)):
    obj = db.get(Equipe, team_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Equipe introuvable")
    return obj

@router.patch("/{team_id}", response_model=EquipeOut)
def update_team(team_id: int, data: EquipeUpdate, db: Session = Depends(get_db)):
    obj = db.get(Equipe, team_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Equipe introuvable")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/{team_id}", status_code=204)
def delete_team(team_id: int, db: Session = Depends(get_db)):
    obj = db.get(Equipe, team_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Equipe introuvable")
    db.delete(obj)
    db.commit()
