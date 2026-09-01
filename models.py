from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base=declarative_base()

class Ticket(Base):
    __tablename__="tickets"
    id=Column(Integer, primary_key=True)
    titlu=Column(String)
    descriere=Column(String)
    status=Column(String, default="nou")
