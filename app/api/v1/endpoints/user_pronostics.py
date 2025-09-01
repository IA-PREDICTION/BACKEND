from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.user_pronostic import PronosticUtilisateur
from app.schemas.user_pronostic import PronosticCreate, PronosticOut, PronosticUpdate
from app.models.user import Utilisateur
from app.core.deps import get_current_user
from app.services.quota import consume_daily_pronostic_quota

router = APIRouter()

@router.post("/", response_model=PronosticOut, status_code=201)
def create_pronostic(
    payload: PronosticCreate,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user),
):
    # 1) verrou / reset / check / consommation du quota
    quota_info = consume_daily_pronostic_quota(db, current_user.id)

    # 2) empêcher les doublons pour un match
    existing = db.query(PronosticUtilisateur).filter_by(
        user_id=current_user.id, match_id=payload.match_id
    ).first()
    if existing:
        # si on veut "restituer" la conso du quota en cas d'échec ici,
        # pas besoin : tout est dans la même transaction => rollback automatique
        raise HTTPException(status_code=400, detail="Déjà un prono pour ce match")

    # 3) créer le prono (la transaction englobe quota + insert)
    prono = PronosticUtilisateur(user_id=current_user.id, **payload.dict())
    db.add(prono)
    db.commit()          # commit atomique: conso quota + prono ensemble
    db.refresh(prono)

    # (option) tu peux renvoyer les infos de quota dans les headers
    # via Response/JSONResponse si tu veux; ici on s'en tient au body standard
    return prono


@router.get("/", response_model=List[PronosticOut])
def list_pronostics(
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user),
):
    return db.query(PronosticUtilisateur).filter_by(user_id=current_user.id).all()


@router.get("/{prono_id}", response_model=PronosticOut)
def get_pronostic(
    prono_id: int,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user),
):
    prono = db.query(PronosticUtilisateur).filter_by(id=prono_id, user_id=current_user.id).first()
    if not prono:
        raise HTTPException(status_code=404, detail="Pronostic introuvable")
    return prono


@router.put("/{prono_id}", response_model=PronosticOut)
def update_pronostic(
    prono_id: int,
    payload: PronosticUpdate,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user),
):
    prono = db.query(PronosticUtilisateur).filter_by(id=prono_id, user_id=current_user.id).first()
    if not prono:
        raise HTTPException(status_code=404, detail="Pronostic introuvable")
    for k, v in payload.dict(exclude_unset=True).items():
        setattr(prono, k, v)
    db.commit()
    db.refresh(prono)
    return prono


@router.delete("/{prono_id}", status_code=204)
def delete_pronostic(
    prono_id: int,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user),
):
    prono = db.query(PronosticUtilisateur).filter_by(id=prono_id, user_id=current_user.id).first()
    if not prono:
        raise HTTPException(status_code=404, detail="Pronostic introuvable")
    db.delete(prono)
    db.commit()
    return None
