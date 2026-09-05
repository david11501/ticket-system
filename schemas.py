from pydantic import BaseModel

class TicketCreate(BaseModel):
    titlu: str
    descriere: str

class UserCreate(BaseModel):
    username: str
    parola: str
    rol: str
    nume: str=None
    specializare: str=None

class LoginRequest(BaseModel):
    username: str
    parola: str