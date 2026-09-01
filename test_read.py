from database import SessionLocal
from models import Ticket

db=SessionLocal()

toate_tichetele=db.query(Ticket).all()

for t in toate_tichetele:
    print(f"ID:{t.id} | Titlu: {t.titlu} | Descriere {t.descriere} | Status:{t.status}")

db.close()