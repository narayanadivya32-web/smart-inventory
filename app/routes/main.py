from fastapi import FastAPI
from dotenv import load_dotenv
import os

from app.routes.reports import router as reports_router
from app.routes.products import router as products_router
from app.routes.movements import router as movements_router
from app.routes.auth import router as auth_router

# ✅ Load environment variables
load_dotenv()

app = FastAPI(title="Smart Inventory")

app.include_router(products_router)
app.include_router(movements_router)
app.include_router(auth_router)
app.include_router(reports_router)

@app.get("/health")
def health():
    return {"status": "ok"}