from database import SessionLocal
from models import Ticket

db=SessionLocal()

tichet_nou=Ticket(
    titlu="motorul nu porneste",
    descriere="motorul de pe linia 3 nu raspunde la nicio comanda",
    status="nou"
)

db.add(tichet_nou)
db.commit()

print("Tichet salvat cu id:",tichet_nou.id)

db.close()