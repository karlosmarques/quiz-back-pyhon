from fastapi import APIRouter, Depends, HTTPException
from  schemas import Quiztitulo,QuizPerguntas, Quizalternativas
from dependencies import pegar_sesao, verificartokem
from models import Quizzes,User,Questions,Answers




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
            raise HTTPException (status_code=401, detail="você não é adm para poder fazer isso!")
        
        session.add(quizdados_novo)
        session.commit()
        raise HTTPException(status_code=201, detail = f"Quiz {quizdados.titulo} criado com sucesso!")
   else:
         raise HTTPException(status_code=401, detail = "Erro ao criar o quiz!")
       
@order_router.post('/questions')
async def criar_perguntas(quizperguntas: Quiztitulo, session = Depends(pegar_sesao), usuario:User = Depends(verificartokem)):
    quizperguntas_novo = Questions(texto=quizperguntas.texto)
    p = session.query(Questions).filter_by(texto = quizperguntas.texto).first()
    if not p:
        if not usuario.is_admin:
                raise HTTPException (status_code=401, detail="você não é adm para poder fazer isso!")
        session.add(quizperguntas_novo)
        session.commit()
        raise HTTPException(status_code=201, detail="enviado com sucesso")
    else:
         raise HTTPException(status_code=401, detail = "Erro ao criar pergunta")

@order_router.post('/answers')
async def  criar_alternativas(quizallternativas: Quizalternativas, session = Depends(pegar_sesao), usuario:User = Depends (verificartokem)):
     quizalternativas_novo =Answers (quiz_id = quizallternativas.question_id, texto= quizallternativas.texto, correta= quizallternativas.correta)
     a = session.query(Answers).filter_by(texto = quizallternativas.texto).first()
     if not a: 
         if not usuario.is_admin:
                raise HTTPException (status_code=401, detail="você não é adm para poder fazer isso!")
         session.add(quizalternativas_novo)
         session.commit()
         raise HTTPException(status_code=201, detail="enviado com sucesso")
     else:
         raise HTTPException(status_code=401, detail = "Erro ao criar pergunta")
     
@order_router.post("/quizzes/cancelar/{id}")
async def cancelar_quiz(id:int, session = Depends(pegar_sesao),usuario:User = Depends (verificartokem)):
    quizzes_delete = session.query(Quizzes).filter(Quizzes.id==id).first()
    if not quizzes_delete:
          raise HTTPException(status_code=400, detail="Quiz não encontrado")
    if not usuario.is_admin:
                raise HTTPException (status_code=401, detail="você não é adm para poder fazer isso!")
    session.delete(quizzes_delete)
    session.commit()
    return {"detail": f"Quiz com ID {id} foi apagado com sucesso!"}