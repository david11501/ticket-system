from fastapi import FastAPI
from database import SessionLocal
from models import Ticket

app= FastAPI()

@app.get("/tickets")
def get_tickets():
    db=SessionLocal()
    tichete=db.query(Ticket).all()
    db.close()
    return tichete
