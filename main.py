from typing import Optional

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(title="Hola API")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

RATE_LIMIT = "10/minute"


class PersonaIn(BaseModel):
    nombre: str
    apellido: str
    email: str
    edad: Optional[int] = None


class Persona(PersonaIn):
    id: int


personas: dict[int, Persona] = {}
next_id = 1


@app.get("/")
def read_root():
    return {"message": "Hola"}


@app.post("/personas", response_model=Persona, status_code=201)
@limiter.limit(RATE_LIMIT)
def crear_persona(request: Request, datos: PersonaIn):
    global next_id
    persona = Persona(id=next_id, **datos.model_dump())
    personas[persona.id] = persona
    next_id += 1
    return persona


@app.get("/personas", response_model=list[Persona])
@limiter.limit(RATE_LIMIT)
def listar_personas(request: Request):
    return list(personas.values())


@app.get("/personas/{persona_id}", response_model=Persona)
@limiter.limit(RATE_LIMIT)
def obtener_persona(request: Request, persona_id: int):
    if persona_id not in personas:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    return personas[persona_id]


@app.put("/personas/{persona_id}", response_model=Persona)
@limiter.limit(RATE_LIMIT)
def modificar_persona(request: Request, persona_id: int, datos: PersonaIn):
    if persona_id not in personas:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    persona = Persona(id=persona_id, **datos.model_dump())
    personas[persona_id] = persona
    return persona


@app.delete("/personas/{persona_id}", status_code=204)
@limiter.limit(RATE_LIMIT)
def eliminar_persona(request: Request, persona_id: int):
    if persona_id not in personas:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    del personas[persona_id]
