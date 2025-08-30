from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.joueur import Joueur
from app.schemas.joueur import JoueurCreate, JoueurOut, JoueurUpdate

router = APIRouter()

@router.post("/", response_model=JoueurOut, status_code=201)
def create_player(data: JoueurCreate, db: Session = Depends(get_db)):
    obj = Joueur(**data.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@router.get("/", response_model=list[JoueurOut])
def list_players(
    db: Session = Depends(get_db),
    equipe_id: int | None = None,
    actif: bool | None = None,
    limit: int = Query(100, le=500),
):
    q = db.query(Joueur)
    if equipe_id is not None: q = q.filter(Joueur.equipe_id == equipe_id)
    if actif is not None: q = q.filter(Joueur.actif == actif)
    return q.limit(limit).all()

@router.get("/{player_id}", response_model=JoueurOut)
def get_player(player_id: int, db: Session = Depends(get_db)):
    obj = db.get(Joueur, player_id)
    if not obj: raise HTTPException(status_code=404, detail="Joueur introuvable")
    return obj

@router.patch("/{player_id}", response_model=JoueurOut)
def update_player(player_id: int, data: JoueurUpdate, db: Session = Depends(get_db)):
    obj = db.get(Joueur, player_id)
    if not obj: raise HTTPException(status_code=404, detail="Joueur introuvable")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit(); db.refresh(obj)
    return obj

@router.delete("/{player_id}", status_code=204)
def delete_player(player_id: int, db: Session = Depends(get_db)):
    obj = db.get(Joueur, player_id)
    if not obj: return
    db.delete(obj); db.commit()
