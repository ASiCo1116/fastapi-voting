from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import crud, database, oauth2, schemas

router = APIRouter(prefix="/vote", tags=["Vote"])


@router.get("/", status_code=status.HTTP_201_CREATED)
def vote(
    vote: schemas.Vote,
    db: Annotated[Session, Depends(database.get_db)],
    current_user: Annotated[schemas.UserOut, Depends(oauth2.get_current_user)],
):
    found_post = crud.get_post_by_id(db, vote.post_id)
    if not found_post:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, f"Post with id {vote.post_id} does not exist."
        )

    found_vote = crud.get_vote(db, vote.post_id, current_user.id)
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(
                status.HTTP_409_CONFLICT,
                f"User {current_user.id} has already voted on post {vote.post_id}.",
            )
        msg = crud.create_vote(db, vote.post_id, current_user.id)
        return msg
    else:
        if not found_vote:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Vote does not exist.")
        msg = crud.delete_vote(db, vote.post_id, current_user.id)
        return msg
