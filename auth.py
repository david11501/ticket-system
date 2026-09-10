from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException
from database import SessionLocal
from models import User
from fastapi import Cookie

pwd_context=CryptContext(schemes=["bcrypt"])

SECRET_KEY="cheia-secreta-schimba-asta"
ALGORITHM="HS256"

def hash_parola(parola):
    return pwd_context.hash(parola)

def verifica_parola(parola, parola_hash):
    return pwd_context.verify(parola, parola_hash)

def creeaza_token(username):
    expira=datetime.utcnow() + timedelta(hours=8)
    payload={"sub": username, "exp": expira}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

security=HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials= Depends(security)):
    token=credentials.credentials
    db=SessionLocal()
    try:
        payload = jwt.decode(token, SECRET_KEY , algorithms=[ALGORITHM])
        username=payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token invalid")
        user_logat=db.query(User).filter(User.username==username).first()
        if not user_logat:
            raise HTTPException(status_code=401, detail="Token invalid")
        return user_logat
    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalid sau expirat")

def get_current_user_cookie(access_token :str=Cookie(None)):
    if not access_token:
        raise HTTPException(status_code=401, detail="Nu esti autentificat")
    db=SessionLocal()
    try:
        payload= jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        username=payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token invalid")
        user_logat=db.query(User).filter(User.username==username).first()
        if not user_logat:
            raise HTTPException(status_code=401, detail="Token invalid")
        return user_logat
    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalid sau expirat")