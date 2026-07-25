# Hola API

API mínima en [FastAPI](https://fastapi.tiangolo.com/) que devuelve un saludo.

## Uso

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/` | Devuelve `{"message": "Hola"}` |
| POST | `/personas` | Alta de persona |
| GET | `/personas` | Listado de personas |
| GET | `/personas/{id}` | Obtener una persona |
| PUT | `/personas/{id}` | Modificación de persona |
| DELETE | `/personas/{id}` | Baja de persona |

Campos de persona: `nombre`, `apellido`, `email`, `edad` (opcional).

Los endpoints de `/personas` tienen rate limit de **10 requests por minuto** por IP (responden `429 Too Many Requests` al superarlo).

## Persistencia

Los datos se guardan en SQLite (`personas.db`, se crea solo al arrancar) usando [SQLModel](https://sqlmodel.tiangolo.com/). Para migrar a PostgreSQL alcanza con cambiar `DATABASE_URL` en `main.py`.

Documentación interactiva en `http://127.0.0.1:8000/docs`.
