from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.core.config import settings
from app.db.session import get_db
from app.models.user import Utilisateur

# Le endpoint de login que tu exposes déjà
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> Utilisateur:
    cred_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Identifiants invalides",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        sub = payload.get("sub")
        user_id = int(sub) if sub is not None else None
        if not user_id:
            raise cred_exc
    except JWTError:
        raise cred_exc

    user = db.get(Utilisateur, user_id)
    if not user:
        raise cred_exc
    return user

# def _get_user(db: Session, token_dep):
#     from fastapi import Depends
#     token = Depends(token_dep)
#     try:
#         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
#         sub = payload.get("sub")
#         if sub is None:
#             raise ValueError
#         user = db.query(Utilisateur).get(int(sub))
#         if not user:
#             raise ValueError
#         return user
#     except Exception:
#         raise HTTPException(status_code=401, detail="Token invalide")
