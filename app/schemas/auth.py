from pydantic import BaseModel, EmailStr

class RegisterIn(BaseModel):
    nom: str
    email: EmailStr
    mot_de_passe: str

class LoginIn(BaseModel):
    email: EmailStr
    mot_de_passe: str

class TokenOut(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
