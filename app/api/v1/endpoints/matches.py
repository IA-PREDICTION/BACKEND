from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.db.session import get_db
from app.models.match import Match
from app.schemas.match import MatchCreate, MatchOut, MatchUpdate

router = APIRouter()

@router.post("/", response_model=MatchOut, status_code=201)
def create_match(data: MatchCreate, db: Session = Depends(get_db)):
    obj = Match(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("/", response_model=list[MatchOut])
def list_matches(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = Query(50, le=100),
    sport_id: int | None = None,
    championnat_id: int | None = None,
    statut: str | None = None
):
    q = db.query(Match)
    if sport_id: q = q.filter(Match.sport_id == sport_id)
    if championnat_id: q = q.filter(Match.championnat_id == championnat_id)
    if statut: q = q.filter(Match.statut == statut)
    return q.order_by(Match.date_match.asc()).offset(skip).limit(limit).all()

@router.get("/today", response_model=list[MatchOut])
def matches_today(db: Session = Depends(get_db)):
    # On considère la journée courante en UTC pour rester simple.
    # (Tu pourras ajuster au fuseau "Africa/Abidjan" si besoin.)
    now = datetime.now(timezone.utc)
    start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=1)
    q = db.query(Match).filter(and_(Match.date_match >= start, Match.date_match < end))
    return q.order_by(Match.date_match.asc()).all()

@router.get("/{match_id}", response_model=MatchOut)
def get_match(match_id: int, db: Session = Depends(get_db)):
    obj = db.get(Match, match_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Match introuvable")
    return obj

@router.patch("/{match_id}", response_model=MatchOut)
def update_match(match_id: int, data: MatchUpdate, db: Session = Depends(get_db)):
    obj = db.get(Match, match_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Match introuvable")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/{match_id}", status_code=204)
def delete_match(match_id: int, db: Session = Depends(get_db)):
    obj = db.get(Match, match_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Match introuvable")
    db.delete(obj)
    db.commit()
