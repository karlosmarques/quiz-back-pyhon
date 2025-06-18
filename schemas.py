from pydantic import BaseModel, EmailStr
from typing import Optional

class Credenciais(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    data_nascimento: str
    is_admin: Optional[bool] = False

    class Config:
        from_attributes = True

class loginSchema(BaseModel):
    email: EmailStr
    senha: str

    class Config:
        from_attributes = True

class Quiztitulo(BaseModel):
    titulo: str
    criado_por: int

    class config:
        from_attributes = True
        
class QuizPerguntas(BaseModel):
    quiz_id: str
    texto: str
    
    class config:
        from_attributes = True
            
    
class Quizalternativas(BaseModel):
    question_id: str
    texto: str
    correta: bool