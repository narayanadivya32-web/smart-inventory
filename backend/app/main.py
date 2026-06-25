from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from app.routes.main import router as main_router
from app.routes.products import router as products_router
from app.routes.movements import router as movements_router
from app.routes.auth import router as auth_router
from app.routes.reports import router as reports_router

app = FastAPI(title="Smart Inventory")

# ✅ CORS FIX (THIS IS WHAT YOU WERE MISSING)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",
        "http://127.0.0.1:4200"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# routers
app.include_router(main_router)
app.include_router(products_router)
app.include_router(movements_router)
app.include_router(auth_router)
app.include_router(reports_router)