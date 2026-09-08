from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base=declarative_base()

class Ticket(Base):
    __tablename__="tickets"
    id=Column(Integer, primary_key=True)
    titlu=Column(String)
    descriere=Column(String)
    status=Column(String, default="nou")
    severitate=Column(String, nullable=True)
    categorie=Column(String, nullable=True)
    sfaturi=Column(String, nullable=True)
    inginer_id=Column(Integer, nullable=True)
    adnotari=Column(String, nullable=True)

class Inginer(Base):
    __tablename__="ingineri"
    id=Column(Integer, primary_key=True)
    nume=Column(String)
    specializare=Column(String)
    nr_tichete_active=Column(Integer,default=0)

class User(Base):
    __tablename__="users"
    id=Column(Integer, primary_key=True)
    username=Column(String, unique=True)
    password_hash=Column(String)
    rol=Column(String)
    inginer_id=Column(Integer, nullable=True)
