from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.deps import get_current_user
from app.models.reaction import Reaction
from app.models.commentaire import Commentaire
from app.models.user_pronostic import PronosticUtilisateur
from app.schemas.reactions import ReactionToggleIn, ReactionOut

router = APIRouter()

@router.post("/toggle", response_model=ReactionOut)
def toggle_reaction(payload: ReactionToggleIn, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if not payload.commentaire_id and not payload.pronostic_id:
        raise HTTPException(400, "commentaire_id ou pronostic_id requis")

    # Valider cible
    if payload.commentaire_id:
        if not db.get(Commentaire, payload.commentaire_id):
            raise HTTPException(404, "Commentaire introuvable")
        existing = db.query(Reaction).filter(
            Reaction.user_id == user.id,
            Reaction.commentaire_id == payload.commentaire_id
        ).first()
    else:
        if not db.get(PronosticUtilisateur, payload.pronostic_id):
            raise HTTPException(404, "Pronostic introuvable")
        existing = db.query(Reaction).filter(
            Reaction.user_id == user.id,
            Reaction.pronostic_id == payload.pronostic_id
        ).first()

    if existing:
        # si même type -> toggle off (supprimer), sinon switch de type
        if existing.type == payload.type:
            db.delete(existing); db.commit()
            raise HTTPException(204, detail=None)
        else:
            existing.type = payload.type
            db.add(existing); db.commit(); db.refresh(existing)
            return existing
    else:
        r = Reaction(
            user_id=user.id,
            commentaire_id=payload.commentaire_id,
            pronostic_id=payload.pronostic_id,
            type=payload.type
        )
        db.add(r); db.commit(); db.refresh(r)
        return r
