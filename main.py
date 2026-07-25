from fastapi import FastAPI

app = FastAPI(title="Hola API")


@app.get("/")
def read_root():
    return {"message": "Hola"}
