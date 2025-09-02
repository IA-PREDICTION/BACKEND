from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Optional
from app.db.session import get_db
from app.core.deps import get_current_user
from app.core.permissions import require_admin
from app.models.commentaire import Commentaire, StatutComment
from app.schemas.comments import CommentCreate, CommentUpdate, CommentOut, CommentList

router = APIRouter()

@router.post("/", response_model=CommentOut, status_code=201)
def create_comment(payload: CommentCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if not payload.match_id and not payload.pronostic_id:
        raise HTTPException(400, "match_id ou pronostic_id requis")
    c = Commentaire(
        user_id=user.id,
        match_id=payload.match_id,
        pronostic_id=payload.pronostic_id,
        parent_id=payload.parent_id,
        contenu=payload.contenu,
    )
    db.add(c); db.commit(); db.refresh(c)
    return c

@router.get("/", response_model=CommentList)
def list_comments(
    db: Session = Depends(get_db),
    match_id: Optional[int] = None,
    pronostic_id: Optional[int] = None,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    q = db.query(Commentaire).filter(Commentaire.statut == StatutComment.visible)
    if match_id: q = q.filter(Commentaire.match_id == match_id)
    if pronostic_id: q = q.filter(Commentaire.pronostic_id == pronostic_id)
    total = q.count()
    items = q.order_by(Commentaire.created_at.desc()).offset(offset).limit(limit).all()
    return {"items": items, "total": total}

@router.patch("/{comment_id}", response_model=CommentOut)
def update_comment(comment_id: int, payload: CommentUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    c = db.get(Commentaire, comment_id)
    if not c: raise HTTPException(404, "Commentaire introuvable")
    # auteur ou admin
    if c.user_id != user.id:
        try:
            require_admin(user)
        except HTTPException:
            raise HTTPException(403, "Accès refusé")

    if payload.contenu is not None:
        c.contenu = payload.contenu
    if payload.statut is not None:
        # statut via admin uniquement
        require_admin(user)
        c.statut = payload.statut

    db.add(c); db.commit(); db.refresh(c)
    return c

@router.delete("/{comment_id}", status_code=204)
def delete_comment(comment_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    c = db.get(Commentaire, comment_id)
    if not c: raise HTTPException(404, "Commentaire introuvable")
    if c.user_id != user.id:
        require_admin(user)
    db.delete(c); db.commit()
    return
