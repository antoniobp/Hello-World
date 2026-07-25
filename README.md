# Hola API

API mínima en [FastAPI](https://fastapi.tiangolo.com/) que devuelve un saludo.

## Uso

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## Endpoints

| Método | Ruta | Respuesta |
|--------|------|-----------|
| GET | `/` | `{"message": "Hola"}` |

Documentación interactiva en `http://127.0.0.1:8000/docs`.
