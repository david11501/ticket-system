# Ticket System

Sistem de gestionare a tichetelor tehnice pentru companii industriale, dezvoltat ca proiect de practică în cadrul proiectului **ROBO-STEP** (Stagii de practică în Mecatronică și Robotică, UPT).

Un utilizator poate semnala o problemă tehnică printr-un tichet, care este clasificat automat de un model de inteligență artificială (severitate + categorie), primind fie sfaturi automate de rezolvare, fie fiind asignat automat inginerului potrivit, în funcție de specializare și de încărcarea curentă de lucru.

## Funcționalități

- **Creare tichete** — descriere liberă a problemei, clasificată automat prin LLM
- **Clasificare AI** — severitate (ușor/major) și categorie (mecanic, electric, optic, software), cu sfaturi generate automat
- **Asignare automată** — tichetele majore sunt atribuite inginerului cu specializarea potrivită și cele mai puține tichete active
- **Autentificare** — înregistrare și login cu parole criptate (bcrypt) și token-uri JWT
- **Roluri diferite** — creator (creează tichete, vede istoric propriu) și inginer (vede tichetele asignate, actualizează status și adnotări)
- **Rute protejate** — acces restricționat pe baza rolului utilizatorului autentificat
- **Interfață web** — login, dashboard (grupat pe status: nou / în lucru / rezolvat), creare și actualizare tichete

## Stack tehnic

| Componentă | Tehnologie |
|---|---|
| Backend | Python, FastAPI |
| Bază de date | SQLite, SQLAlchemy (ORM) |
| Validare date | Pydantic |
| Inteligență artificială | Claude API (Anthropic) |
| Autentificare | JWT (python-jose), bcrypt (passlib) |
| Frontend | Jinja2 Templates, HTML, CSS |
| Control versiuni | Git / GitHub |

## Rulare locală

```bash
# clonare
git clone https://github.com/david11501/ticket-system.git
cd ticket-system

# mediu virtual
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux

# instalare dependințe
pip install fastapi uvicorn sqlalchemy pydantic anthropic python-dotenv passlib[bcrypt] python-jose[cryptography] jinja2 python-multipart

# variabile de mediu (.env)
ANTHROPIC_API_KEY=cheia-ta-aici

# pornire server
uvicorn main:app --reload
```

Aplicația pornește la `http://127.0.0.1:8000`, cu redirecționare automată către pagina de autentificare.

Documentația interactivă a API-ului (Swagger UI) e disponibilă la `http://127.0.0.1:8000/docs`.

## Arhitectură — fluxul unui tichet

1. Un utilizator cu rol **creator** trimite un tichet (titlu + descriere)
2. Descrierea e trimisă către modelul Claude, care returnează severitate, categorie și sfaturi
3. Dacă severitatea e **ușoară**, tichetul primește sfaturile automat
4. Dacă severitatea e **majoră**, sistemul caută inginerul cu specializarea potrivită și cele mai puține tichete active, și îi asignează tichetul
5. Inginerul vede tichetul în dashboard, poate adăuga adnotări și actualiza statusul (nou → în lucru → rezolvat)
6. Creatorul poate urmări în orice moment istoricul și starea tichetelor proprii

## Context

Proiect dezvoltat integral ca parte a stagiului de practică ROBO-STEP, cofinanțat de Uniunea Europeană prin Programul Educație și Ocupare.