from database import SessionLocal
from models import Inginer

db=SessionLocal()

db.add(Inginer(nume='Andrei', specializare="software", nr_tichete_active=0))
db.add(Inginer(nume='Cristi', specializare="electric", nr_tichete_active=0))
db.add(Inginer(nume='Maria', specializare="mecanic", nr_tichete_active=0))
db.add(Inginer(nume='Beni', specializare="optic", nr_tichete_active=0))

db.commit()
db.close()
print("Ingineri adaugati")