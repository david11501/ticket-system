from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

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
