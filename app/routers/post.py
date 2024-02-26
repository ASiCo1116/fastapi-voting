from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from .. import crud, database, oauth2, schemas

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[schemas.PostOut])
def get_posts(
    db: Annotated[Session, Depends(database.get_db)],
    limit: int = 10,
    skip: int = 0,
    search: str | None = "",
):
    posts = crud.get_posts(db, limit, skip, search)
    return posts


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Post)
def get_post(db: Annotated[Session, Depends(database.get_db)], id: int):
    post = crud.get_post_by_id(db, id)
    if not post:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, f"post with id: {id} was not found."
        )
    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(
    post: schemas.PostCreate,
    db: Annotated[Session, Depends(database.get_db)],
    current_user: Annotated[schemas.UserOut, Depends(oauth2.get_current_user)],
):
    new_post = crud.create_post(post, db, current_user)
    return new_post


@router.delete("/{id}")
def delete_post(
    id: int,
    db: Annotated[Session, Depends(database.get_db)],
    current_user: Annotated[schemas.UserOut, Depends(oauth2.get_current_user)],
):
    post = crud.get_post_by_id(db, id)

    if not post:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"Post with id: {id} was not found.",
        )

    if post.owner_id != current_user.id:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            "Not authorized to perform requseted action.",
        )

    crud.delete_post(id, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(
    id: int,
    update_post: schemas.PostCreate,
    db: Annotated[Session, Depends(database.get_db)],
    current_user: Annotated[schemas.UserOut, Depends(oauth2.get_current_user)],
):
    post = crud.get_post_by_id(db, id)

    if not post:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"Post with id: {id} was not found.",
        )

    if post.owner_id != current_user.id:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            "Not authorized to perform requseted action.",
        )

    update_post = crud.update_post(id, update_post, db)

    return update_post
