from fastapi import APIRouter, Depends, HTTPException
from  schemas import Quiztitulo,QuizPerguntas, Quizalternativas,ResponderQuizSchema
from dependencies import pegar_sesao, verificartokem
from models import Quizzes,User,Questions,Answers,Respostas_usuarios
from sqlalchemy.orm import joinedload,Session




order_router = APIRouter(prefix="/quizes", tags=["quizes"])




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
async def criar_perguntas(quizperguntas: QuizPerguntas, session = Depends(pegar_sesao), usuario:User = Depends(verificartokem)):
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
     
@order_router.post("/quizzes/deletar/{id}")
async def deletar_quiz(id:int, session = Depends(pegar_sesao),usuario:User = Depends (verificartokem)):
    quizzes_delete = session.query(Quizzes).filter(Quizzes.id==id).first()
    if not quizzes_delete:
          raise HTTPException(status_code=400, detail="Quiz não encontrado")
    if not usuario.is_admin:
                raise HTTPException (status_code=401, detail="você não é adm para poder fazer isso!")
    session.delete(quizzes_delete)
    session.commit()
    return {"detail": f"Quiz com ID {id} foi apagado com sucesso!"}

@order_router.get("/quizzes/{id}")
async def pegar_quizzes(id:int,session = Depends(pegar_sesao)):
     quizzes = session.query(Quizzes).options(joinedload(Quizzes.questions).joinedload(Questions.answers)).filter(Quizzes.id ==id).first()
     if not quizzes:
        raise HTTPException(status_code=404, detail="Quiz não encontrado")
     return quizzes

@order_router.get("/listaquiz")
async def pegar_quizzes(session = Depends(pegar_sesao)):
     quizzes = session.query(Quizzes).options(joinedload(Quizzes.questions).joinedload(Questions.answers)).all()
     if not quizzes:
        raise HTTPException(status_code=404, detail="Quiz não encontrado")
     return quizzes


@order_router.get('/usuario') 
async def exibe_usuario(usuario: User = Depends(verificartokem)):
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    return {
        "message": "Usuário encontrado",
        "usuario": {
            "nome": usuario.nome,
            "email": usuario.email
        }
    }


@order_router.post('/responder-quiz')
async def responder_quiz(
    resposta: ResponderQuizSchema,
    session: Session = Depends(pegar_sesao),
    usuario: User = Depends(verificartokem)
):
    if not resposta.quiz_id or resposta.score is None:
        raise HTTPException(status_code=400, detail="quiz_id e score são obrigatórios")

    try:
        nova_resposta = Respostas_usuarios(
            quiz_id=resposta.quiz_id,
            user_id=usuario.id,
            score=resposta.score
        )

        session.add(nova_resposta)
        session.commit()
        session.refresh(nova_resposta)

        return {"message": "Pontuação salva com sucesso", "respostaUsuario": {
            "id": nova_resposta.id,
            "quiz_id": nova_resposta.quiz_id,
            "user_id": nova_resposta.user_id,
            "score": nova_resposta.score
        }}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Erro ao salvar pontuação")