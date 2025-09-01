from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.db.session import get_db

from app.schemas.predict import PredictRequest, PredictResponse
from app.models.features_engineering import FeaturesEngineering
from app.models.prediction import Prediction
from app.models.prediction_log import LogPrediction
from app.models.ml_model import ModeleIA
from decimal import Decimal

router = APIRouter()

def _to_jsonable(x):
    if isinstance(x, Decimal):
        return float(x)
    if isinstance(x, dict):
        return {k: _to_jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_to_jsonable(v) for v in x]
    return x

def _dummy_model_infer(type_prediction: str, feats: dict) -> dict:
    """
    Mock: calcule des probas simples à partir de quelques features si présentes.
    Retourne un dict prêt à passer à Prediction(**dict).
    """
    out: dict = {
        "type_prediction": type_prediction,
        "prediction_finale": None,
        "confidence": None,
        "proba_victoire_dom": None,
        "proba_nul": None,
        "proba_victoire_ext": None,
        "score_predit_dom": None,
        "score_predit_ext": None,
        "total_buts_predit": None,
        "proba_over_2_5": None,
        "proba_under_2_5": None,
        "proba_btts_oui": None,
        "proba_btts_non": None,
    }

    # On “pondère” légèrement selon elo/xg si dispo
    elo_dom = float(feats.get("elo_rating_dom", 1500))
    elo_ext = float(feats.get("elo_rating_ext", 1500))
    xg_dom = float(feats.get("xg_rolling_dom", 1.2))
    xg_ext = float(feats.get("xg_rolling_ext", 1.1))

    if type_prediction == "match_result":
        # score ELO diff + petit boost par xg
        diff = (elo_dom - elo_ext) / 400.0  # environ
        base_dom = 0.33 + 0.15 * diff + 0.05 * (xg_dom - 1.0)
        base_ext = 0.33 - 0.15 * diff + 0.05 * (xg_ext - 1.0)
        base_nul = 1.0 - (base_dom + base_ext)

        # clamp
        pd = max(0.05, min(0.9, base_dom))
        pe = max(0.05, min(0.9, base_ext))
        pn = max(0.05, min(0.9, base_nul))
        s = pd + pn + pe
        pd, pn, pe = pd/s, pn/s, pe/s

        out["proba_victoire_dom"] = round(pd, 2)
        out["proba_nul"] = round(pn, 2)
        out["proba_victoire_ext"] = round(pe, 2)

        # prédiction finale = argmax
        if pd >= pn and pd >= pe:
            out["prediction_finale"] = "1"
            out["confidence"] = out["proba_victoire_dom"]
        elif pe >= pd and pe >= pn:
            out["prediction_finale"] = "2"
            out["confidence"] = out["proba_victoire_ext"]
        else:
            out["prediction_finale"] = "X"
            out["confidence"] = out["proba_nul"]

    elif type_prediction == "over_under":
        total = xg_dom + xg_ext
        out["total_buts_predit"] = round(total, 2)
        # heuristique simple
        p_over = min(0.95, max(0.05, 0.2 + 0.3 * (total - 2.0)))
        p_under = 1.0 - p_over
        out["proba_over_2_5"] = round(p_over, 2)
        out["proba_under_2_5"] = round(p_under, 2)
        out["prediction_finale"] = "OVER" if p_over >= p_under else "UNDER"
        out["confidence"] = max(out["proba_over_2_5"], out["proba_under_2_5"])

    elif type_prediction == "both_teams_score":
        # probas BTTS selon xg moyens
        p_yes = min(0.95, max(0.05, (xg_dom/1.5)*0.5 + (xg_ext/1.5)*0.5))
        p_no = 1.0 - p_yes
        out["proba_btts_oui"] = round(p_yes, 2)
        out["proba_btts_non"] = round(p_no, 2)
        out["prediction_finale"] = "BTTS_OUI" if p_yes >= p_no else "BTTS_NON"
        out["confidence"] = max(out["proba_btts_oui"], out["proba_btts_non"])

    else:  # score_exact
        # un petit 1-0 “par défaut” si elo_dom > elo_ext, sinon 1-1
        if elo_dom >= elo_ext:
            out["score_predit_dom"] = 1
            out["score_predit_ext"] = 0
            out["prediction_finale"] = "1-0"
            out["confidence"] = 0.55
        else:
            out["score_predit_dom"] = 1
            out["score_predit_ext"] = 1
            out["prediction_finale"] = "1-1"
            out["confidence"] = 0.5

    return out

@router.post("/", response_model=PredictResponse, status_code=201)
def predict(payload: PredictRequest, db: Session = Depends(get_db)):
    # 1) Vérif modèle existe
    model = db.get(ModeleIA, payload.modele_id)
    if not model:
        raise HTTPException(status_code=404, detail="Modèle introuvable")

    # 2) Features: override > DB > défauts
    feats: dict = {}
    if payload.override_features:
        feats = dict(payload.override_features or {})
    else:
        fe = db.query(FeaturesEngineering).filter(
            and_(
                FeaturesEngineering.match_id == payload.match_id,
                FeaturesEngineering.modele_id == payload.modele_id
            )
        ).first()
        if fe:
            # On extrait quelques features utiles, on pourrait aussi tout sérialiser
            feats = {
                "elo_rating_dom": fe.elo_rating_dom,
                "elo_rating_ext": fe.elo_rating_ext,
                "xg_rolling_dom": fe.xg_rolling_dom,
                "xg_rolling_ext": fe.xg_rolling_ext,
            }

    # 3) Inference mockée
    infer = _dummy_model_infer(payload.type_prediction, feats)

    # 4) Ecriture Prediction
    pred = Prediction(
        match_id=payload.match_id,
        modele_id=payload.modele_id,
        **infer
    )
    db.add(pred); db.commit(); db.refresh(pred)

    # 5) Log
    log = LogPrediction(
        prediction_id=pred.id,
        match_id=payload.match_id,
        modele_id=payload.modele_id,
        input_features=_to_jsonable(feats),   # <-- ici
        output_raw=_to_jsonable(infer),       # <-- et ici
        temps_inference_ms=5,
        version_api="mock-1.0",
        erreur=None
    )
    db.add(log); db.commit()

    return PredictResponse(
        prediction_id=pred.id,
        match_id=pred.match_id,
        modele_id=pred.modele_id,
        type_prediction=pred.type_prediction,
        prediction_finale=pred.prediction_finale,
        confidence=float(pred.confidence) if pred.confidence is not None else None,
        proba_victoire_dom=float(pred.proba_victoire_dom) if pred.proba_victoire_dom is not None else None,
        proba_nul=float(pred.proba_nul) if pred.proba_nul is not None else None,
        proba_victoire_ext=float(pred.proba_victoire_ext) if pred.proba_victoire_ext is not None else None,
    )
