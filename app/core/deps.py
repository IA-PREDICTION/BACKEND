from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.core.config import settings
from app.db.session import get_db
from app.models.user import Utilisateur

def get_current_user(db: Session = Depends(get_db), token: str = Depends(lambda: None)):
    # On récupère le token du header Authorization ci-dessous avec un Security scheme léger
    from fastapi import Header
    async def _token(authorization: str | None = Header(default=None)):
        if not authorization or not authorization.lower().startswith("bearer "):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token manquant")
        return authorization.split(" ", 1)[1]
    return _get_user(db, token_dep=_token)

def _get_user(db: Session, token_dep):
    from fastapi import Depends
    token = Depends(token_dep)
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        sub = payload.get("sub")
        if sub is None:
            raise ValueError
        user = db.query(Utilisateur).get(int(sub))
        if not user:
            raise ValueError
        return user
    except Exception:
        raise HTTPException(status_code=401, detail="Token invalide")
