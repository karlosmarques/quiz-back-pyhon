from models import db
from main import secret_key, algorithm, oauth2_schema
from sqlalchemy.orm import sessionmaker, session
from models import User
from fastapi import Depends, HTTPException
from jose import jwt, JWTError

def pegar_sesao():
    Session = sessionmaker(bind=db)
    session = Session()
    try:
        yield session
    finally:
        session.close()

def verificartokem(token = Depends(oauth2_schema), session = Depends(pegar_sesao)):
    try:
     dic_info =jwt.decode(token,secret_key,algorithm)
     id_usuario = dic_info.get(id)
    except JWTError:
       raise HTTPException(status_code=401, detail="Acesso negado, verifique o validade do token")
    usuario  = session.query(User).filter(User.id == id_usuario).first()
    if not usuario:
       raise HTTPException(status_code=401,detail="Acesso Invalido!")
    
    return usuario
