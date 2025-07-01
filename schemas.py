from pydantic import BaseModel, EmailStr
from typing import Optional, List

class Credenciais(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    is_admin: Optional[bool] = False

    class Config:
        orm_mode = True

class loginSchema(BaseModel):
    email: EmailStr
    senha: str

    class Config:
        orm_mode = True

class Quizalternativas(BaseModel):
    question_id: int
    texto: str
    correta: bool

    class Config:
        orm_mode = True

class QuizPerguntas(BaseModel):
    quiz_id: int
    texto: str
    alternativas: List[Quizalternativas]

    class Config:
        orm_mode = True

class Quiztitulo(BaseModel):
    titulo: str
    criado_por: int
    perguntas: List[QuizPerguntas]

    class Config:
        orm_mode = True

class usuário(BaseModel):
    userID:int
    nome:str
    email:EmailStr

    class Config:
        orm_mode= True



class ResponderQuizSchema(BaseModel):
    quiz_id: int
    score: float

    class Config:
        orm_mode= True
