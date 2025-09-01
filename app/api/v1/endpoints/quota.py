from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.db.session import get_db
from app.core.deps import get_current_user
from app.models.user import Utilisateur
from app.services.subscriptions import get_active_subscription

router = APIRouter()

@router.get("/pronostics-journalier")
def get_daily_pronostic_quota(
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user),
):
    abn, plan = get_active_subscription(db, current_user.id)
    if not abn or not plan:
        raise HTTPException(status_code=403, detail="Aucun abonnement actif")

    if plan.nb_pronostics_jour is None:
        return {"limit": None, "used": None, "remaining": None, "reset_on": abn.date_reset_quotidien}

    used = abn.nb_pronostics_jour_utilises or 0
    limit = plan.nb_pronostics_jour
    remaining = max(0, limit - used)
    return {
        "limit": limit,
        "used": used,
        "remaining": remaining,
        "reset_on": abn.date_reset_quotidien,
    }
