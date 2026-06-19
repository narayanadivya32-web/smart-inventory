
from fastapi import FastAPI

app = FastAPI()

from app.routes import main  # if you have routes

@app.get("/")
def root():
    return {"message": "API is running"}