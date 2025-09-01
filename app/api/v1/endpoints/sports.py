from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.sport import Sport
from app.schemas.sport import SportCreate, SportOut, SportUpdate

router = APIRouter()

@router.post("/", response_model=SportOut, status_code=201)
def create_sport(data: SportCreate, db: Session = Depends(get_db)):
    if db.query(Sport).filter((Sport.nom == data.nom) | (Sport.code == data.code)).first():
        raise HTTPException(status_code=400, detail="Sport déjà existant (nom ou code)")
    obj = Sport(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("/", response_model=list[SportOut])
def list_sports(db: Session = Depends(get_db), skip: int = 0, limit: int = Query(50, le=100)):
    return db.query(Sport).offset(skip).limit(limit).all()

@router.get("/{sport_id}", response_model=SportOut)
def get_sport(sport_id: int, db: Session = Depends(get_db)):
    obj = db.get(Sport, sport_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Sport introuvable")
    return obj

@router.patch("/{sport_id}", response_model=SportOut)
def update_sport(sport_id: int, data: SportUpdate, db: Session = Depends(get_db)):
    obj = db.get(Sport, sport_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Sport introuvable")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/{sport_id}", status_code=204)
def delete_sport(sport_id: int, db: Session = Depends(get_db)):
    obj = db.get(Sport, sport_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Sport introuvable")
    db.delete(obj)
    db.commit()
