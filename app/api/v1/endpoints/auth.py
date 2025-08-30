from fastapi import APIRouter, Depends, HTTPException, status, Request, Header
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from app.db.session import get_db
from app.schemas.auth import RegisterIn, LoginIn, TokenOut
from app.schemas.user import UtilisateurOut
from app.core.security import get_password_hash, verify_password, create_access_token, create_refresh_token
from app.models.user import Utilisateur
from app.models.session_user import SessionUtilisateur, DeviceType
from app.core.config import settings

router = APIRouter()

@router.post("/register", response_model=UtilisateurOut, status_code=201)
def register(data: RegisterIn, db: Session = Depends(get_db)):
    if db.query(Utilisateur).filter(Utilisateur.email == data.email).first():
        raise HTTPException(status_code=400, detail="Email déjà utilisé")
    user = Utilisateur(
        nom=data.nom,
        email=data.email,
        mot_de_passe_hash=get_password_hash(data.mot_de_passe),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/login", response_model=TokenOut)
def login(data: LoginIn, request: Request, db: Session = Depends(get_db)):
    user = db.query(Utilisateur).filter(Utilisateur.email == data.email).first()
    if not user or not verify_password(data.mot_de_passe, user.mot_de_passe_hash):
        raise HTTPException(status_code=400, detail="Identifiants invalides")
    access = create_access_token(user.id)
    refresh = create_refresh_token(user.id)
    # enregistre la session
    sess = SessionUtilisateur(
        user_id=user.id,
        token_session=access,
        refresh_token=refresh,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
        device_type=DeviceType.web,
        expire_at=datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )
    db.add(sess)
    db.commit()
    return {"access_token": access, "refresh_token": refresh, "token_type": "bearer"}


@router.get("/me", response_model=UtilisateurOut)
def me(authorization: str | None = Header(default=None), db: Session = Depends(get_db)):
    # 1) Récupérer le header Authorization
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Token manquant")

    token = authorization.split(" ", 1)[1]

    # 2) Décoder le JWT
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        sub = payload.get("sub")
        if not sub:
            raise HTTPException(status_code=401, detail="Token invalide")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalide")

    # 3) Charger l'utilisateur
    user = db.query(Utilisateur).get(int(sub))
    if not user:
        raise HTTPException(status_code=401, detail="Utilisateur introuvable")

    return user
