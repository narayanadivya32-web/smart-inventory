from datetime import datetime, timedelta
from jose import jwt
from app.config import SECRET_KEY, ALGORITHM


def create_access_token(username):
    expire = datetime.utcnow() + timedelta(minutes=15)

    payload = {
        "sub": username,
        "exp": expire,
        "type": "access"
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def create_refresh_token(username):
    expire = datetime.utcnow() + timedelta(days=7)

    payload = {
        "sub": username,
        "exp": expire,
        "type": "refresh"
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )