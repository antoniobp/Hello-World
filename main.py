from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from sqlmodel import Field, Session, SQLModel, create_engine, select

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(title="Hola API")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

RATE_LIMIT = "10/minute"

DATABASE_URL = "sqlite:///personas.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


class PersonaIn(SQLModel):
    nombre: str
    apellido: str
    email: str
    edad: Optional[int] = None


class Persona(PersonaIn, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


@app.on_event("startup")
def crear_tablas():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


@app.get("/")
def read_root():
    return {"message": "Hola"}


@app.post("/personas", response_model=Persona, status_code=201)
@limiter.limit(RATE_LIMIT)
def crear_persona(request: Request, datos: PersonaIn, session: Session = Depends(get_session)):
    persona = Persona(**datos.model_dump())
    session.add(persona)
    session.commit()
    session.refresh(persona)
    return persona


@app.get("/personas", response_model=list[Persona])
@limiter.limit(RATE_LIMIT)
def listar_personas(request: Request, session: Session = Depends(get_session)):
    return session.exec(select(Persona)).all()


@app.get("/personas/{persona_id}", response_model=Persona)
@limiter.limit(RATE_LIMIT)
def obtener_persona(request: Request, persona_id: int, session: Session = Depends(get_session)):
    persona = session.get(Persona, persona_id)
    if persona is None:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    return persona


@app.put("/personas/{persona_id}", response_model=Persona)
@limiter.limit(RATE_LIMIT)
def modificar_persona(
    request: Request, persona_id: int, datos: PersonaIn, session: Session = Depends(get_session)
):
    persona = session.get(Persona, persona_id)
    if persona is None:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    for campo, valor in datos.model_dump().items():
        setattr(persona, campo, valor)
    session.add(persona)
    session.commit()
    session.refresh(persona)
    return persona


@app.delete("/personas/{persona_id}", status_code=204)
@limiter.limit(RATE_LIMIT)
def eliminar_persona(request: Request, persona_id: int, session: Session = Depends(get_session)):
    persona = session.get(Persona, persona_id)
    if persona is None:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    session.delete(persona)
    session.commit()
