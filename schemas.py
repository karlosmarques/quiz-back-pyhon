from pydantic import BaseModel, EmailStr
from typing import Optional, List

class Credenciais(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    is_admin: Optional[bool] = False

    class Config:
        from_attributes = True
class loginSchema(BaseModel):
    email: EmailStr
    senha: str

    class Config:
        from_attributes = True

class Quizalternativas(BaseModel):
    question_id: int
    texto: str
    correta: bool

    class Config:
        from_attributes = True

class QuizPerguntas(BaseModel):
    quiz_id: int
    texto: str
    alternativas: List[Quizalternativas]

    class Config:
        from_attributes = True

class Quiztitulo(BaseModel):
    titulo: str
    criado_por: int
    perguntas: List[QuizPerguntas]

    class Config:
        from_attributes = True
