from models import Inginer

def gaseste_inginer(categorie,db):
    ingineri_potriviti= db.query(Inginer).filter(Inginer.specializare==categorie).all()
    try:
        if not ingineri_potriviti:
            raise ValueError("nu exista ingineri in acest departament.")
        inginer_ales=min(ingineri_potriviti, key=lambda i: i.nr_tichete_active)
        inginer_ales.nr_tichete_active+=1
        return inginer_ales
    except ValueError as e:
        print(f"erroarea este: {e}")
