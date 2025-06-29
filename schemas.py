from pydantic import BaseModel, EmailStr
from typing import Optional
from typing import List

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
        
    
class Quizalternativas(BaseModel):
    question_id: int
    texto: str
    correta: bool

class QuizPerguntas(BaseModel):
    quiz_id: int
    texto: str
    alternativas: list[Quizalternativas]
    
    class config:
        from_attributes = True


class Quiztitulo(BaseModel):
    titulo: str
    criado_por: int
    perguntas: list[QuizPerguntas]


    class config:
        from_attributes = True