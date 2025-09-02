from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.models.reaction import TypeReaction
from typing import Optional

class ReactionToggleIn(BaseModel):
    commentaire_id: Optional[int] = None
    pronostic_id: Optional[int] = None
    type: TypeReaction

class ReactionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    commentaire_id: Optional[int]
    pronostic_id: Optional[int]
    type: TypeReaction
    created_at: datetime
