from pydantic import BaseModel

class FeaturesEngBase(BaseModel):
    match_id: int
    modele_id: int
    # Tous les champs numériques sont optionnels
    forme_dom_5: float | None = None
    forme_dom_10: float | None = None
    moyenne_buts_marques_dom: float | None = None
    moyenne_buts_encaisses_dom: float | None = None
    clean_sheets_dom_5: int | None = None
    forme_ext_5: float | None = None
    forme_ext_10: float | None = None
    moyenne_buts_marques_ext: float | None = None
    moyenne_buts_encaisses_ext: float | None = None
    clean_sheets_ext_5: int | None = None
    h2h_victoires_dom: int | None = None
    h2h_nuls: int | None = None
    h2h_victoires_ext: int | None = None
    h2h_moyenne_buts: float | None = None
    jours_repos_dom: int | None = None
    jours_repos_ext: int | None = None
    nb_blesses_dom: int | None = None
    nb_blesses_ext: int | None = None
    importance_match_dom: int | None = None
    importance_match_ext: int | None = None
    elo_rating_dom: float | None = None
    elo_rating_ext: float | None = None
    xg_rolling_dom: float | None = None
    xg_rolling_ext: float | None = None
    features_custom: dict | None = None
    version_pipeline: str | None = None

class FeaturesEngCreate(FeaturesEngBase): pass
class FeaturesEngUpdate(FeaturesEngBase): pass  # on autorise upsert via PATCH

class FeaturesEngOut(FeaturesEngBase):
    id: int
    class Config:
        from_attributes = True
