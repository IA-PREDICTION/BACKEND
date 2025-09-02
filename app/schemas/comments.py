from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.models.commentaire import StatutComment

class CommentBase(BaseModel):
    contenu: str
    match_id: Optional[int] = None
    pronostic_id: Optional[int] = None
    parent_id: Optional[int] = None

class CommentCreate(CommentBase):
    pass

class CommentUpdate(BaseModel):
    contenu: Optional[str] = None
    statut: Optional[StatutComment] = None

class CommentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    match_id: Optional[int]
    pronostic_id: Optional[int]
    parent_id: Optional[int]
    contenu: str
    likes: int
    signalements: int
    statut: StatutComment
    created_at: datetime
    updated_at: datetime

class CommentList(BaseModel):
    items: List[CommentOut]
    total: int
