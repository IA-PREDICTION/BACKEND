from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.feature_store_meta import FeatureStoreMeta
from app.schemas.feature_store_meta import FeatureMetaCreate, FeatureMetaOut, FeatureMetaUpdate

router = APIRouter()

@router.post("/", response_model=FeatureMetaOut, status_code=201)
def create_feature_meta(data: FeatureMetaCreate, db: Session = Depends(get_db)):
    if db.query(FeatureStoreMeta).filter(FeatureStoreMeta.nom_feature == data.nom_feature).first():
        raise HTTPException(status_code=400, detail="Feature déjà existante")
    obj = FeatureStoreMeta(**data.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@router.get("/", response_model=list[FeatureMetaOut])
def list_feature_meta(db: Session = Depends(get_db), limit: int = Query(200, le=1000)):
    return db.query(FeatureStoreMeta).limit(limit).all()

@router.patch("/{feature_id}", response_model=FeatureMetaOut)
def update_feature_meta(feature_id: int, data: FeatureMetaUpdate, db: Session = Depends(get_db)):
    obj = db.get(FeatureStoreMeta, feature_id)
    if not obj: raise HTTPException(status_code=404, detail="Feature introuvable")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit(); db.refresh(obj)
    return obj

@router.delete("/{feature_id}", status_code=204)
def delete_feature_meta(feature_id: int, db: Session = Depends(get_db)):
    obj = db.get(FeatureStoreMeta, feature_id)
    if not obj: return
    db.delete(obj); db.commit()
