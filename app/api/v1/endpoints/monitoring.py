from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.db.session import get_db
from app.models.model_monitoring import ModelMonitoring
from app.schemas.model_monitoring import MonitoringCreate, MonitoringOut, MonitoringUpdate
from datetime import datetime

from sqlalchemy import func
from app.models.log_activite import LogActivite
from app.models.metrique_systeme import MetriqueSysteme
from app.models.notification import Notification, TypeNotif, CanalNotif, PrioriteNotif
from app.models.erreur_application import ErreurApplication, NiveauErreur
from app.core.deps import get_current_user  # JWT déjà dispo

router = APIRouter()

router = APIRouter()

@router.post("/", response_model=MonitoringOut, status_code=201)
def upsert_monitoring(data: MonitoringCreate, db: Session = Depends(get_db)):
    obj = db.query(ModelMonitoring).filter(
        and_(ModelMonitoring.modele_id == data.modele_id, ModelMonitoring.date_evaluation == data.date_evaluation)
    ).first()
    if obj:
        for k, v in data.model_dump().items():
            setattr(obj, k, v)
        db.commit(); db.refresh(obj)
        return obj
    obj = ModelMonitoring(**data.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@router.get("/by_model", response_model=list[MonitoringOut])
def get_monitoring_by_model(modele_id: int, db: Session = Depends(get_db)):
    return db.query(ModelMonitoring).filter(ModelMonitoring.modele_id == modele_id).order_by(ModelMonitoring.date_evaluation.desc()).all()

# ---------- Logs activité ----------
@router.post("/logs/activity")
def add_activity_log(
    type_action: str,
    endpoint: str = "",
    methode: str = "",
    duree_ms: int | None = None,
    code_reponse: int | None = None,
    metadata: dict | None = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    log = LogActivite(
        user_id=current_user.id if current_user else None,
        type_action=type_action,
        endpoint=endpoint,
        methode=methode,
        ip_address=None,
        user_agent=None,
        duree_ms=duree_ms,
        code_reponse=code_reponse,
        metadata=metadata
    )
    db.add(log); db.commit()
    return {"ok": True}

# ---------- Métriques ----------
@router.post("/metrics")
def push_metric(
    type_metrique: str,
    valeur: float,
    unite: str | None = None,
    service: str | None = None,
    tags: dict | None = None,
    db: Session = Depends(get_db)
):
    row = MetriqueSysteme(
        type_metrique=type_metrique,
        valeur=valeur,
        unite=unite,
        service=service,
        tags=tags
    )
    db.add(row); db.commit()
    return {"ok": True}

# ---------- Notifications ----------
@router.post("/notifications/send")
def send_notification(
    user_id: int,
    titre: str,
    message: str,
    type: TypeNotif = TypeNotif.promotion,
    canal: CanalNotif = CanalNotif.in_app,
    priorite: PrioriteNotif = PrioriteNotif.normale,
    donnees_contexte: dict | None = None,
    db: Session = Depends(get_db),
):
    notif = Notification(
        user_id=user_id,
        type=type,
        titre=titre,
        message=message,
        lue=False,
        canal=canal,
        priorite=priorite,
        donnees_contexte=donnees_contexte,
        date_envoi=datetime.utcnow()
    )
    db.add(notif); db.commit()
    return {"ok": True, "id": notif.id}

@router.get("/notifications/me")
def my_notifications(
    only_unread: bool = True,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    q = db.query(Notification).filter(Notification.user_id == current_user.id)
    if only_unread:
        q = q.filter(Notification.lue == False)
    return [
        {
            "id": n.id, "titre": n.titre, "message": n.message, "type": n.type.value,
            "lue": n.lue, "priorite": n.priorite.value, "date_envoi": n.date_envoi
        } for n in q.order_by(Notification.created_at.desc()).limit(50).all()
    ]

@router.post("/notifications/mark-read")
def mark_read(
    notif_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    n = db.query(Notification).filter(
        Notification.id == notif_id, Notification.user_id == current_user.id
    ).first()
    if not n:
        raise HTTPException(status_code=404, detail="notification not found")
    n.lue = True
    n.date_lecture = datetime.utcnow()
    db.commit()
    return {"ok": True}

# ---------- Erreurs ----------
@router.post("/errors/report")
def report_error(
    service: str,
    niveau: NiveauErreur,
    message: str,
    stack_trace: str | None = None,
    context: dict | None = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    err = ErreurApplication(
        service=service,
        niveau=niveau,
        message=message,
        stack_trace=stack_trace,
        user_id=(current_user.id if current_user else None),
        context=context
    )
    db.add(err); db.commit()
    return {"ok": True, "id": err.id}

