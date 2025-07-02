from fastapi import APIRouter, Depends, HTTPException
from  schemas import Quiztitulo,ResponderQuizSchema,PerguntaAtualizar
from dependencies import pegar_sesao, verificartokem
from models import Quizzes,User,Questions,Answers,Respostas_usuarios,RespostaUsuarioItem
from sqlalchemy.orm import joinedload, Session




order_router = APIRouter(prefix="/quizes", tags=["quizes"])

@order_router.get('/usuario') 
async def exibe_usuario(usuario: User = Depends(verificartokem)):
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario

@order_router.post('/quizzes')
async def criar_quiz_completo(quizdados: Quiztitulo,session=Depends(pegar_sesao),usuario: User = Depends(verificartokem)):
    if not usuario.is_admin:
        raise HTTPException(status_code=401, detail="Você não é adm para poder fazer isso!")
    novo_quiz = Quizzes(titulo=quizdados.titulo, criado_por=usuario.id)
    session.add(novo_quiz)
    session.commit()
    session.refresh(novo_quiz)

    for pergunta in quizdados.perguntas:
        nova_pergunta = Questions(texto=pergunta.texto,quiz_id=novo_quiz.id)
        session.add(nova_pergunta)
        session.commit()
        session.refresh(nova_pergunta)

        for opcao in pergunta.opcoes:
            nova_alternativa = Answers(texto=opcao.texto,question_id=nova_pergunta.id)
            session.add(nova_alternativa)
    session.commit()
    return {novo_quiz.id}

@order_router.delete("/quizzes/deletar/{id}")
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
         
@order_router.post('/responder-quiz')
async def responder_quiz(resposta: ResponderQuizSchema,session: Session = Depends(pegar_sesao),usuario: User = Depends(verificartokem)):
    if not resposta.quiz_id or not resposta.respostas:
        raise HTTPException(status_code=400, detail="quiz_id e respostas são obrigatórios")

    try:
        # Busca perguntas e respostas corretas
        perguntas = session.query(Questions).options(joinedload(Questions.answers)).filter(Questions.quiz_id == resposta.quiz_id).all()

        respostas_corretas = {
            pergunta.id: next((a.id for a in pergunta.answers if a.correta), None)
            for pergunta in perguntas
        }

        # Calcula acertos
        acertos = 0
        for item in resposta.respostas:
            if respostas_corretas.get(item.question_id) == item.answer_id:
                acertos += 1

        total = len(perguntas)
        score = (acertos / total) * 100 if total > 0 else 0

        # Salva score geral
        nova_resposta = Respostas_usuarios(
            quiz_id=resposta.quiz_id,
            user_id=usuario.id,
            score=score
        )
        session.add(nova_resposta)
        session.commit()
        session.refresh(nova_resposta)

        # Salva respostas individuais
        respostas_itens = [
            RespostaUsuarioItem(
                resposta_usuario_id=nova_resposta.id,
                question_id=item.question_id,
                answer_id=item.answer_id
            ) for item in resposta.respostas
        ]
        session.add_all(respostas_itens)
        session.commit()

        # Lista de erros detalhados
        erros_detalhados = [
            {
                "question_id": item.question_id,
                "resposta_correta": respostas_corretas.get(item.question_id)
            }
            for item in resposta.respostas
            if respostas_corretas.get(item.question_id) != item.answer_id
        ]

        return {
            "message": "Respostas registradas com sucesso",
            "resultado": {
                "total": total,
                "acertos": acertos,
                "erros": total - acertos,
                "score": f"{score:.1f}%",
                "errosDetalhados": erros_detalhados
            }
        }

    except Exception as e:
        print("[ERRO AO REGISTRAR RESPOSTAS]", e)
        raise HTTPException(status_code=500, detail="Erro ao registrar respostas")
    

@order_router.put("/questions/{id}")
async def atualizar_pergunta(id: int,dados: PerguntaAtualizar,session: Session = Depends(pegar_sesao),usuario=Depends(verificartokem)):
    if not usuario.is_admin:
        raise HTTPException(status_code=401, detail="Acesso não autorizado")
    pergunta = session.query(Questions).filter(Questions.id == id).first()
    if not pergunta:
        raise HTTPException(status_code=404, detail="Pergunta não encontrada")
    pergunta.texto = dados.texto
    session.commit()

    for resposta in dados.answers:
        if resposta.id:
            alternativa = session.query(Answers).filter(Answers.id == resposta.id, Answers.question_id == id).first()
            if alternativa:
                alternativa.texto = resposta.texto
                alternativa.correta = resposta.correta
        else:
            nova = Answers(
                texto=resposta.texto,
                correta=resposta.correta,
                question_id=id
            )
            session.add(nova)
    session.commit()
    return {"detail": f"Pergunta {id} atualizada com sucesso"}



