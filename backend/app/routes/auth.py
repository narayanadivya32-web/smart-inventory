from fastapi import APIRouter, HTTPException
from jose import jwt, JWTError

from app.database import get_connection
from app.utils.password import verify_password
from app.security import (
    create_access_token,
    create_refresh_token,
    SECRET_KEY,
    ALGORITHM,
)

router = APIRouter()


# ---------------- LOGIN ----------------
@router.post("/api/auth/token")
def login(data: dict):

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        raise HTTPException(
            status_code=400,
            detail="Username and password are required"
        )

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT username, password_hash
        FROM users
        WHERE username = %s
        """,
        (username,)
    )

    user = cur.fetchone()

    cur.close()
    conn.close()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    db_username = user[0]
    password_hash = user[1]

    if not verify_password(password, password_hash):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    access_token = create_access_token(db_username)
    refresh_token = create_refresh_token(db_username)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


# ---------------- REFRESH TOKEN ----------------
@router.post("/api/auth/refresh")
def refresh_token(data: dict):

    token = data.get("refresh_token")

    if not token:
        raise HTTPException(
            status_code=400,
            detail="Refresh token is required"
        )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=401,
                detail="Invalid refresh token"
            )

        username = payload.get("sub")

        access_token = create_access_token(username)

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token"
        )