from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import crud, schemas, utils
from ..database import get_db

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/")
def get_users(db: Annotated[Session, Depends(get_db)]):
    users = crud.get_users(db)
    return users


@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Annotated[Session, Depends(get_db)]):
    user = crud.get_user_by_id(id, db)
    if not user:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"User with id: {id} does not exist.",
        )
    return user


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Annotated[Session, Depends(get_db)]):
    user.password = utils.hash(user.password)
    new_user = crud.create_user(user, db)
    return new_user
