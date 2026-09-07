from fastapi import FastAPI
from database import SessionLocal
from models import Ticket
from schemas import TicketCreate
from llm import clasificare_tichet
from assignare import gaseste_inginer
from models import User
from schemas import UserCreate
from auth import hash_parola
from models import Inginer
from auth import verifica_parola, creeaza_token
from schemas import LoginRequest
from auth import get_current_user
from fastapi import Depends, HTTPException

app= FastAPI()

@app.get("/tickets")
def get_tickets(current_user: User =Depends(get_current_user)):
    if current_user.rol!="inginer":
        raise HTTPException(status_code=403, detail="Doar inginerii pot vedea tichetele")
    db=SessionLocal()
    tichete=db.query(Ticket).all()
    db.close()
    return tichete

@app.post("/tickets")
def create_ticket(ticket: TicketCreate,current_user: User=Depends(get_current_user)):
    if current_user.rol!="creator":
        raise HTTPException(status_code=403, detail="Doar creatorii pot adauga tichete")
    db=SessionLocal()
    rezultat_llm=clasificare_tichet(ticket.descriere)
    tichet_nou=Ticket(
        titlu=ticket.titlu,
        descriere=ticket.descriere,
        status="nou",
        severitate=rezultat_llm["severitate"],
        categorie=rezultat_llm["categorie"],
        sfaturi="; ".join(rezultat_llm["sfaturi"])
    )

    if rezultat_llm["severitate"]=="major":
        inginer_gasit=gaseste_inginer(rezultat_llm["categorie"],db)
        tichet_nou.inginer_id=inginer_gasit.id
        pass
    db.add(tichet_nou)
    db.commit()
    db.refresh(tichet_nou)
    db.close()
    return tichet_nou


@app.post("/users")
def register(user: UserCreate):
    db=SessionLocal()
    password=hash_parola(user.parola)

    inginer_id_gasit=None

    try:
        if user.rol not in ["creator","inginer"]:
            raise ValueError(f"Rolul de {user.rol} nu exista!")

        if user.rol=="inginer":
            inginer_nou=Inginer(
                nume=user.nume,
                specializare=user.specializare,
                nr_tichete_active=0,
            )
            db.add(inginer_nou)
            db.commit()
            db.refresh(inginer_nou)
            inginer_id_gasit=inginer_nou.id
    except ValueError as e:
        print(e)
        return{"eroare": str(e)}
    user_nou=User(
    username=user.username,
    password_hash=password,
    rol=user.rol,
    inginer_id=inginer_id_gasit
    )
    db.add(user_nou)
    db.commit()
    db.refresh(user_nou)
    db.close()
    return user_nou

@app.post("/login")
def login(date: LoginRequest):
    db=SessionLocal()
    try:
        user_gasit=db.query(User).filter(User.username==date.username).first()
        if not user_gasit:
            raise ValueError(f"Username-ul: {date.username} nu exista.")
        if not verifica_parola(date.parola, user_gasit.password_hash):
            raise ValueError("Parola introdusa nu este corecta.")
        token=creeaza_token(user_gasit.username)
        return {"acces_token": token}
    except ValueError as e:
        print(f"Erroare: {e}")
        return {"erroare": f"{e}"}