from pydantic import BaseModel, EmailStr
from typing import Optional

class Credenciais(BaseModel):
    email: EmailStr
    senha: str
    nome: str
    data_nascimento: str
    is_admin: Optional[bool] = False

    class Config:
        from_attributes = True

class loginSchema(BaseModel):
    email: EmailStr
    senha: str

    class Config:
        from_attributes = True

class Quizdados(BaseModel):
    titulo: str
    criado_por: int

    class config:
        from_attributes = True