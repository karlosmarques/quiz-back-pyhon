from pydantic import BaseModel, EmailStr,Field
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
    texto: str
    
    class Config:
        from_attributes = True

class QuizPerguntas(BaseModel):
    texto: str
    opcoes: List[Quizalternativas]

    class Config:
        from_attributes = True

class Quiztitulo(BaseModel):
    titulo: str
    perguntas: List[QuizPerguntas]

    class Config:
        from_attributes = True

class RespostaItem(BaseModel):
    question_id: int
    answer_id: int

    class Config:
        from_attributes = True

class ResponderQuizSchema(BaseModel):
    quiz_id: int
    respostas: List[RespostaItem]

    class Config:
        from_attributes = True