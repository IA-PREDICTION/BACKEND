from datetime import datetime, date
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.subscription import Abonnement  # adapte le chemin
from app.services.subscriptions import get_active_subscription

def _today_utc() -> date:
    return datetime.utcnow().date()

def consume_daily_pronostic_quota(db: Session, user_id: int) -> dict:
    """
    Vérifie le quota journalier et consomme 1 unité si possible.
    - Lock pessimiste sur la ligne abonnement (FOR UPDATE)
    - Reset quotidien si nécessaire
    - Incrémente nb_pronostics_jour_utilises
    Retourne des infos de quota (pour logs/headers éventuels).
    """
    today = _today_utc()

    # Lock la ligne d'abonnement actif pour éviter double consommation concurrente
    from app.models.subscription import Abonnement, PlanAbonnement  # local import si besoin
    now = datetime.utcnow()
    abn = (
        db.query(Abonnement)
        .filter(
            Abonnement.user_id == user_id,
            Abonnement.statut == "actif",
            Abonnement.date_debut <= now,
            Abonnement.date_fin >= now,
        )
        .with_for_update()
        .first()
    )

    if not abn:
        raise HTTPException(status_code=403, detail="Aucun abonnement actif")

    plan = db.get(PlanAbonnement, abn.plan_id) if abn.plan_id else None
    # NULL = illimité (comme dans ton schéma)
    daily_limit = None if not plan else plan.nb_pronostics_jour

    # Si illimité => pas de reset ni d'incrément obligatoire (on peut ignorer le compteur)
    if daily_limit is None:
        return {"limit": None, "used": None, "remaining": None, "reset_on": None}

    # Reset quotidien si nécessaire
    if not abn.date_reset_quotidien or abn.date_reset_quotidien != today:
        abn.nb_pronostics_jour_utilises = 0
        abn.date_reset_quotidien = today

    used = abn.nb_pronostics_jour_utilises or 0
    if used >= daily_limit:
        remaining = 0
        raise HTTPException(
            status_code=429,  # Too Many Requests
            detail=f"Quota quotidien atteint ({daily_limit} pronostics/jour). Réinitialisation quotidienne à minuit (UTC).",
        )

    # Consommer 1
    abn.nb_pronostics_jour_utilises = used + 1
    db.add(abn)  # marquer dirty

    return {
        "limit": int(daily_limit),
        "used": int(used + 1),
        "remaining": int(daily_limit - (used + 1)),
        "reset_on": str(today),
    }
