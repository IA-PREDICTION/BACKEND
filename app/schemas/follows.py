from pydantic import BaseModel, ConfigDict
from datetime import datetime

class FollowIn(BaseModel):
    following_id: int

class FollowOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    follower_id: int
    following_id: int
    created_at: datetime
