from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.championnat import Championnat
from app.schemas.championnat import ChampionnatCreate, ChampionnatOut, ChampionnatUpdate

router = APIRouter()

@router.post("/", response_model=ChampionnatOut, status_code=201)
def create_league(data: ChampionnatCreate, db: Session = Depends(get_db)):
    obj = Championnat(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("/", response_model=list[ChampionnatOut])
def list_leagues(db: Session = Depends(get_db), skip: int = 0, limit: int = Query(50, le=100), sport_id: int | None = None):
    q = db.query(Championnat)
    if sport_id:
        q = q.filter(Championnat.sport_id == sport_id)
    return q.offset(skip).limit(limit).all()

@router.get("/{league_id}", response_model=ChampionnatOut)
def get_league(league_id: int, db: Session = Depends(get_db)):
    obj = db.get(Championnat, league_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Championnat introuvable")
    return obj

@router.patch("/{league_id}", response_model=ChampionnatOut)
def update_league(league_id: int, data: ChampionnatUpdate, db: Session = Depends(get_db)):
    obj = db.get(Championnat, league_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Championnat introuvable")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/{league_id}", status_code=204)
def delete_league(league_id: int, db: Session = Depends(get_db)):
    obj = db.get(Championnat, league_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Championnat introuvable")
    db.delete(obj)
    db.commit()
