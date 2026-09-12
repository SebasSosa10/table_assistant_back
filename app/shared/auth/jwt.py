from datetime import datetime, timedelta, timezone

import jwt

from shared.config.settings import settings
from shared.exceptions import UnauthorizedError


def create_access_token(*, user_id: int, email: str, role: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_expire_minutes)
    payload = {
        "sub": str(user_id),
        "email": email,
        "role": role,
        "exp": expire,
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm="HS256")


def decode_access_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
    except jwt.ExpiredSignatureError as exc:
        raise UnauthorizedError("El token ha expirado") from exc
    except jwt.InvalidTokenError as exc:
        raise UnauthorizedError("Token inválido") from exc
