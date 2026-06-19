from fastapi import APIRouter, HTTPException
from jose import jwt, JWTError

from app.database import get_connection
from app.utils.password import verify_password
from app.security import (
    create_access_token,
    create_refresh_token,
    SECRET_KEY,
    ALGORITHM
)

router = APIRouter()


# ---------------- LOGIN ----------------
@router.post("/api/auth/token")
def login(data: dict):
    ...
    # your login logic here


# ---------------- REFRESH TOKEN ----------------
@router.post("/api/auth/refresh")
def refresh_token(data: dict):

    token = data.get("refresh_token")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        username = payload.get("sub")

        new_access_token = create_access_token(username)

        return {
            "access_token": new_access_token,
            "token_type": "bearer"
        }

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")