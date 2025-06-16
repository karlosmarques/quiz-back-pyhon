from fastapi import APIRouter, Depends, HTTPException
from  schemas import Quiztitulo
from dependencies import pegar_sesao, verificartokem
from models import Quizzes,User




order_router = APIRouter(prefix="/quizes", tags=["quizes"])


@order_router.get('/')
async def get_quizes():
    return {"mensagem":"lista de quizes"}

@order_router.post('/quizzes')
async def criar_quiz(quizdados: Quiztitulo, session = Depends(pegar_sesao),usuario:User = Depends(verificartokem)):
   q = session.query(Quizzes).filter_by(titulo=quizdados.titulo).first()
   if not q:
        quizdados_novo = Quizzes(titulo=quizdados.titulo, criado_por=quizdados.criado_por)
        if not usuario.is_admin:
            raise HTTPException (status_code=401, detail="você não é adm para pdedr fazer isso!")
        
        session.add(quizdados_novo)
        session.commit()
        raise HTTPException(status_code=201, detail = f"Quiz {quizdados.titulo} criado com sucesso!")
   else:
         raise HTTPException(status_code=400, detail = "Erro ao criar o quiz!")
       


