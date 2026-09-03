from fastapi import FastAPI
from database import SessionLocal
from models import Ticket
from schemas import TicketCreate

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
    tichet_nou=Ticket(
        titlu=ticket.titlu,
        descriere=ticket.descriere,
        status="nou"
    )
    db.add(tichet_nou)
    db.commit()
    db.refresh(tichet_nou)
    db.close()
    return tichet_nou