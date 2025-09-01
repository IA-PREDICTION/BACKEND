from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.subscription import Abonnement, PlanAbonnement  # adapte les chemins si besoin

def get_active_subscription(db: Session, user_id: int) -> tuple[Abonnement | None, PlanAbonnement | None]:
    """Retourne (abonnement_actif, plan) si trouvé, sinon (None, None)."""
    now = datetime.utcnow()
    abn = (
        db.query(Abonnement)
        .filter(
            Abonnement.user_id == user_id,
            Abonnement.statut == "actif",
            Abonnement.date_debut <= now,
            Abonnement.date_fin >= now,
        )
        .first()
    )
    if not abn:
        return None, None
    plan = db.get(PlanAbonnement, abn.plan_id) if abn.plan_id else None
    return abn, plan
