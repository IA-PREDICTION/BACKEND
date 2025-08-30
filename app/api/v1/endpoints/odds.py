from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.db.session import get_db
from app.models.cote import CoteBookmaker
from app.schemas.cote import CoteCreate, CoteOut, CoteUpdate

router = APIRouter()

@router.post("/", response_model=CoteOut, status_code=201)
def create_odd(data: CoteCreate, db: Session = Depends(get_db)):
    obj = CoteBookmaker(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.post("/bulk_upsert", response_model=list[CoteOut])
def bulk_upsert_odds(payload: list[CoteCreate], db: Session = Depends(get_db)):
    out = []
    for item in payload:
        d = item.model_dump()
        existing = db.query(CoteBookmaker).filter(
            and_(
                CoteBookmaker.match_id == d["match_id"],
                CoteBookmaker.bookmaker == d["bookmaker"],
                CoteBookmaker.date_maj == d["date_maj"],
            )
        ).first()
        if existing:
            # update champs
            for k in ["cote_dom","cote_nul","cote_ext","cote_over_2_5","cote_under_2_5","cote_btts_oui","cote_btts_non"]:
                setattr(existing, k, d.get(k))
            db.add(existing)
            out.append(existing)
        else:
            obj = CoteBookmaker(**d)
            db.add(obj)
            out.append(obj)
    db.commit()
    for o in out:
        db.refresh(o)
    return out

@router.get("/", response_model=list[CoteOut])
def list_odds(
    db: Session = Depends(get_db),
    match_id: int | None = None,
    bookmaker: str | None = None,
    limit: int = Query(100, le=500),
):
    q = db.query(CoteBookmaker)
    if match_id: q = q.filter(CoteBookmaker.match_id == match_id)
    if bookmaker: q = q.filter(CoteBookmaker.bookmaker == bookmaker)
    return q.order_by(CoteBookmaker.date_maj.desc()).limit(limit).all()

@router.patch("/{odd_id}", response_model=CoteOut)
def update_odd(odd_id: int, data: CoteUpdate, db: Session = Depends(get_db)):
    obj = db.get(CoteBookmaker, odd_id)
    if not obj: raise HTTPException(status_code=404, detail="Cote introuvable")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit(); db.refresh(obj)
    return obj

@router.delete("/{odd_id}", status_code=204)
def delete_odd(odd_id: int, db: Session = Depends(get_db)):
    obj = db.get(CoteBookmaker, odd_id)
    if not obj: raise HTTPException(status_code=404, detail="Cote introuvable")
    db.delete(obj); db.commit()
