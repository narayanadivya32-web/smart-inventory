from datetime import datetime, timedelta
from jose import jwt

SECRET_KEY = "smart_inventory_secret_key"
ALGORITHM = "HS256"


def verify_password(plain_password, stored_password):
    return plain_password == stored_password


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