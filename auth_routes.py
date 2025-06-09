from fastapi import APIRouter, Depends
from models import User
from dependencies import pegar_sesao



auth_router = APIRouter(prefix="/auth", tags = ["autenticação"])

@auth_router.post('/')
async def meM():
    return {"mensagem": "Rota de autenticação"}


@auth_router.post('/registro')
async def resgistro_usuario(email:str,senha:str,nome:str, data_nascimento:str, session= Depends(pegar_sesao)):
    user = session.query(User).filter_by(email=email).first()
    if user:
        return {"mensagem": "Usuário já existe"}
    else:
        novo_usuario = User(nome, email, senha, data_nascimento)
        session.add(novo_usuario)
        session.commit()
        return {"mensagem": "Usuário registrado com sucesso"}
