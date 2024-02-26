from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from . import crud, database, schemas
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    jwt_encode = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

    return jwt_encode


def verify_access_token(token: str, credentials_exception):
    try:
        results = jwt.decode(token, SECRET_KEY, ALGORITHM)
        user_id: int = results.get("user_id")

        if not user_id:
            raise credentials_exception

        token_data = schemas.TokenData(id=user_id)

    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(
    db: Annotated[Session, Depends(database.get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = verify_access_token(token, credentials_exception)
    user = crud.get_user_by_id(token_data.id, db)

    return user
