from fastapi import FastAPI
from database import SessionLocal
from models import Ticket
from schemas import TicketCreate
from llm import clasificare_tichet
from assignare import gaseste_inginer
from models import User
from schemas import UserCreate, TicketUpdate
from auth import hash_parola, get_current_user_cookie
from models import Inginer
from auth import verifica_parola, creeaza_token
from schemas import LoginRequest
from auth import get_current_user
from fastapi import Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi import Request,Form
from fastapi.responses import RedirectResponse

templates=Jinja2Templates(directory="templates")

app= FastAPI()

@app.get("/login-form")
def login_form(request: Request):
    return templates.TemplateResponse(request=request, name="login.html")

@app.post("/login-form")
def login_form_submit(username:str=Form(...), parola:str=Form(...)):
    db=SessionLocal()
    try:
        user_gasit=db.query(User).filter(User.username==username).first()
        if not user_gasit or not verifica_parola(parola, user_gasit.password_hash):
            db.close()
            return {"eroare":"Username sau parola incorecta"}
        token=creeaza_token(user_gasit.username)
        response=RedirectResponse(url="/dashboard", status_code=303)
        response.set_cookie(key="access_token", value=token, httponly=True)
        return response
    finally:
        db.close()

@app.get("/tickets")
def get_tickets(current_user: User =Depends(get_current_user)):
    db=SessionLocal()
    try:
        if current_user.rol!="inginer":
            raise HTTPException(status_code=403, detail="Doar inginerii pot vedea tichetele")
        db=SessionLocal()
        tichete=db.query(Ticket).all()
        return tichete
    finally:
        db.close()

@app.get("/my-tickets")
def get_my_tickets(current_user: User=Depends(get_current_user)):
    db=SessionLocal()
    try:
        if current_user.rol!="inginer":
            raise HTTPException(status_code=403, detail="Useru-ul nu este un inginer")
        lista_de_tichete_active=(db.query(Ticket).filter(Ticket.inginer_id==current_user.inginer_id)).all()
        return lista_de_tichete_active
    finally:
        db.close()

@app.post("/tickets")
def create_ticket(ticket: TicketCreate,current_user: User=Depends(get_current_user)):

    try:
        if current_user.rol!="creator":
            raise HTTPException(status_code=403, detail="Doar creatorii pot adauga tichete")
        db=SessionLocal()
        rezultat_llm=clasificare_tichet(ticket.descriere)
        tichet_nou=Ticket(
            creator_id=current_user.id,
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
        return tichet_nou
    finally:
        db.close()


@app.post("/users")
def register(user: UserCreate):
    db = SessionLocal()
    password = hash_parola(user.parola)
    inginer_id_gasit = None
    try:
        if user.rol not in ["creator", "inginer"]:
            raise ValueError(f"Rolul de {user.rol} nu exista!")

        if user.rol == "inginer":
            inginer_nou = Inginer(
                nume=user.nume,
                specializare=user.specializare,
                nr_tichete_active=0,
            )
            db.add(inginer_nou)
            db.commit()
            db.refresh(inginer_nou)
            inginer_id_gasit = inginer_nou.id

        user_nou = User(
            username=user.username,
            password_hash=password,
            rol=user.rol,
            inginer_id=inginer_id_gasit
        )
        db.add(user_nou)
        db.commit()
        db.refresh(user_nou)
        return user_nou
    except ValueError as e:
        print(e)
        return {"eroare": str(e)}
    finally:
        db.close()

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
        return {"access_token": token}
    except ValueError as e:
        print(f"Erroare: {e}")
        return {"erroare": f"{e}"}
    finally:
        db.close()

@app.get("/dashboard")
def dashboard(request: Request, current_user: User=Depends(get_current_user_cookie)):
    db=SessionLocal()
    try:
        if current_user.rol=="inginer":
            tichete=db.query(Ticket).filter(Ticket.inginer_id==current_user.inginer_id).all()
        else:
            tichete=db.query(Ticket).filter(Ticket.creator_id==current_user.id).all()
        return templates.TemplateResponse(
            request=request,
            name="dashboard.html",
            context={"user":current_user, "tichete":tichete}
        )
    finally:
        db.close()

@app.post("/tickets/{id}/update-form")
def update_ticket_form(id: int, status:str=Form(...), adnotari:str=Form(""), current_user:User=Depends(get_current_user_cookie)):
    db=SessionLocal()
    try:
        if current_user.rol!="inginer":
            raise HTTPException(status_code=403, detail="Nu sunteti un inginer.")
        else:
            tichet=db.query(Ticket).filter(Ticket.id==id).first()
            if not tichet:
                raise HTTPException(status_code=404, detail="Tichetul nu exista")
            if tichet.inginer_id!=current_user.inginer_id:
                raise HTTPException(status_code=403, detail="Nu este tichetul dumneavoastra.")
            if status:
                tichet.status=status
            if adnotari:
                tichet.adnotari=adnotari
            db.commit()
            db.refresh(tichet)
            return RedirectResponse(url="/dashboard", status_code=303)
    finally:
        db.close()

@app.put("/tickets/{id}")
def update_ticket(id: int, update: TicketUpdate, current_user: User=Depends(get_current_user)):
    db=SessionLocal()
    try:
        if current_user.rol!="inginer":
            raise HTTPException(status_code=403, detail="User-ul nu este un inginer.")
        tichet=db.query(Ticket).filter(Ticket.id==id).first()
        if not tichet:
            raise HTTPException(status_code=404, detail="Tichetul nu exista")
        if tichet.inginer_id!=current_user.inginer_id:
            raise HTTPException(status_code=403, detail="Nu este id-ul de inginer corect")
        if update.status!=None:
            tichet.status=update.status
        if update.adnotari!=None:
            tichet.adnotari=update.adnotari
        db.commit()
        db.refresh(tichet)
        return tichet
    finally:
            db.close()

@app.get("/my-history")
def get_my_history(current_user: User=Depends(get_current_user)):
    db=SessionLocal()
    try:
        if current_user.rol!="creator":
            raise HTTPException(status_code=403, detail="Nu sunteti creator.")
        toate_tichetele=db.query(Ticket).filter(Ticket.creator_id==current_user.id).all()
        return toate_tichetele
    finally:
        db.close()