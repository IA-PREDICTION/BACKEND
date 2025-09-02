from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.deps import get_current_user
from app.models.suivi import SuiviUtilisateur
from app.models.user import Utilisateur
from app.schemas.follows import FollowIn, FollowOut
from typing import List

router = APIRouter()

@router.post("/", response_model=FollowOut, status_code=201)
def follow_user(payload: FollowIn, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if payload.following_id == user.id:
        raise HTTPException(400, "Impossible de se suivre soi-même")
    if not db.get(Utilisateur, payload.following_id):
        raise HTTPException(404, "Utilisateur à suivre introuvable")
    existing = db.query(SuiviUtilisateur).filter(
        SuiviUtilisateur.follower_id == user.id,
        SuiviUtilisateur.following_id == payload.following_id
    ).first()
    if existing: return existing
    f = SuiviUtilisateur(follower_id=user.id, following_id=payload.following_id)
    db.add(f); db.commit(); db.refresh(f)
    return f

@router.delete("/{following_id}", status_code=204)
def unfollow_user(following_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    existing = db.query(SuiviUtilisateur).filter(
        SuiviUtilisateur.follower_id == user.id,
        SuiviUtilisateur.following_id == following_id
    ).first()
    if not existing:
        raise HTTPException(404, "Suivi non trouvé")
    db.delete(existing); db.commit()
    return

@router.get("/followers/{user_id}", response_model=List[FollowOut])
def list_followers(user_id: int, db: Session = Depends(get_db), limit: int = Query(50, ge=1, le=100), offset: int = Query(0, ge=0)):
    q = db.query(SuiviUtilisateur).filter(SuiviUtilisateur.following_id == user_id)
    return q.order_by(SuiviUtilisateur.created_at.desc()).offset(offset).limit(limit).all()

@router.get("/following/{user_id}", response_model=List[FollowOut])
def list_following(user_id: int, db: Session = Depends(get_db), limit: int = Query(50, ge=1, le=100), offset: int = Query(0, ge=0)):
    q = db.query(SuiviUtilisateur).filter(SuiviUtilisateur.follower_id == user_id)
    return q.order_by(SuiviUtilisateur.created_at.desc()).offset(offset).limit(limit).all()
