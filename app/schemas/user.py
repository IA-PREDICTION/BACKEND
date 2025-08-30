from pydantic import BaseModel, EmailStr

class UtilisateurOut(BaseModel):
    id: int
    nom: str
    email: EmailStr
    role: str
    statut: str

    class Config:
        from_attributes = True   # pydantic v2
