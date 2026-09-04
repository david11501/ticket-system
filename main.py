from fastapi import FastAPI
from database import SessionLocal
from models import Ticket
from schemas import TicketCreate
from llm import clasificare_tichet
from assignare import gaseste_inginer

app= FastAPI()

@app.get("/tickets")
def get_tickets():
    db=SessionLocal()
    tichete=db.query(Ticket).all()
    db.close()
    return tichete

@app.post("/tickets")
def create_ticket(ticket: TicketCreate):
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