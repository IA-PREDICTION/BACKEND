from fastapi import HTTPException, status
from app.models.user import Utilisateur, Role

def require_admin(user: Utilisateur):
    if user.role != Role.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin only")
