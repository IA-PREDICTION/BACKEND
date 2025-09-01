from pydantic import BaseModel

class StatMatchBase(BaseModel):
    match_id: int
    possession_dom: float | None = None
    possession_ext: float | None = None
    tirs_dom: int | None = None
    tirs_ext: int | None = None
    tirs_cadres_dom: int | None = None
    tirs_cadres_ext: int | None = None
    corners_dom: int | None = None
    corners_ext: int | None = None
    fautes_dom: int | None = None
    fautes_ext: int | None = None
    cartons_jaunes_dom: int | None = None
    cartons_jaunes_ext: int | None = None
    cartons_rouges_dom: int | None = None
    cartons_rouges_ext: int | None = None
    xg_dom: float | None = None
    xg_ext: float | None = None
    passes_reussies_dom: int | None = None
    passes_reussies_ext: int | None = None
    hors_jeux_dom: int | None = None
    hors_jeux_ext: int | None = None
    metadata_json: dict | None = None

class StatMatchCreate(StatMatchBase): pass

class StatMatchUpdate(BaseModel):
    # tous facultatifs
    possession_dom: float | None = None
    possession_ext: float | None = None
    tirs_dom: int | None = None
    tirs_ext: int | None = None
    tirs_cadres_dom: int | None = None
    tirs_cadres_ext: int | None = None
    corners_dom: int | None = None
    corners_ext: int | None = None
    fautes_dom: int | None = None
    fautes_ext: int | None = None
    cartons_jaunes_dom: int | None = None
    cartons_jaunes_ext: int | None = None
    cartons_rouges_dom: int | None = None
    cartons_rouges_ext: int | None = None
    xg_dom: float | None = None
    xg_ext: float | None = None
    passes_reussies_dom: int | None = None
    passes_reussies_ext: int | None = None
    hors_jeux_dom: int | None = None
    hors_jeux_ext: int | None = None
    metadata_json: dict | None = None

class StatMatchOut(StatMatchBase):
    id: int
    class Config:
        from_attributes = True
