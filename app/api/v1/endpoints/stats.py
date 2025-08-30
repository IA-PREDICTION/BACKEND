from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.stat_match import StatistiquesMatch
from app.schemas.stat_match import StatMatchCreate, StatMatchOut, StatMatchUpdate

router = APIRouter()

@router.post("/", response_model=StatMatchOut, status_code=201)
def upsert_stats(data: StatMatchCreate, db: Session = Depends(get_db)):
    # 1:1 sur match_id => upsert simple
    obj = db.query(StatistiquesMatch).filter(StatistiquesMatch.match_id == data.match_id).first()
    if obj:
        for k, v in data.model_dump().items():
            setattr(obj, k, v)
        db.commit(); db.refresh(obj)
        return obj
    obj = StatistiquesMatch(**data.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@router.get("/by_match/{match_id}", response_model=StatMatchOut)
def get_stats_by_match(match_id: int, db: Session = Depends(get_db)):
    obj = db.query(StatistiquesMatch).filter(StatistiquesMatch.match_id == match_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Statistiques introuvables")
    return obj

@router.delete("/by_match/{match_id}", status_code=204)
def delete_stats(match_id: int, db: Session = Depends(get_db)):
    obj = db.query(StatistiquesMatch).filter(StatistiquesMatch.match_id == match_id).first()
    if not obj: return
    db.delete(obj); db.commit()
