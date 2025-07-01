from main import secret_key, algorithm 
from fastapi import APIRouter, Depends, HTTPException
from models import User
from dependencies import pegar_sesao, verificartokem
from main import bcrypt_context
from schemas import Credenciais,loginSchema
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone


auth_router = APIRouter(prefix="/auth", tags = ["autenticação"])


def criar_token(id, email, is_admin):
    data_expiração = datetime.now(timezone.utc) + timedelta(minutes=120)
    disc_info ={"id":id, "email": email, "is_admin": is_admin, "exp": data_expiração}
    jwt_decodificado = jwt.encode(disc_info,key=secret_key, algorithm=algorithm)
    return jwt_decodificado


def autenticar_usuario(email, senha, session):
    user  = session.query(User).filter(User.email == email).first()
    if not user:
        return False
    if not bcrypt_context.verify(senha, user.senha):
        return False
    return user




@auth_router.post('/')
async def meM():
    return {"mensagem": "Rota de autenticação"}


@auth_router.post('/registro')
async def resgistro_usuario(credenciais: Credenciais, session= Depends(pegar_sesao)):
    user = session.query(User).filter_by(email=credenciais.email).first()
    if user:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    else:
        senha_hash = bcrypt_context.hash(credenciais.senha)
        novo_usuario = User(credenciais.nome, credenciais.email, senha_hash,credenciais.is_admin)
        session.add(novo_usuario)
        session.commit()
        return HTTPException(status_code=201, detail=f"Usuário cadastrado com sucesso! {novo_usuario.email}")
    

@auth_router.post('/login')
async def login_usuario(login: loginSchema,session =Depends(pegar_sesao)):
    user = autenticar_usuario(login.email, login.senha, session)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    else:
        access_token = criar_token(id=user.id, email=user.email, is_admin=user.is_admin)
        return {"id": user.id,"role": "ADMIN" if user.is_admin else "USER","token": access_token
    }
    
    

    
    


