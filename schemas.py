from pydantic import BaseModel

class TicketCreate(BaseModel):
    titlu: str
    descriere: str