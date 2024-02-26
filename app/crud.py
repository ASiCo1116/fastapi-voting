from sqlalchemy import func
from sqlalchemy.orm import Session

from . import models, schemas


def get_posts(
    db: Session,
    limit: int,
    skip: int,
    search: str | None,
):
    # join posts and votes table to get vote counts
    posts = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .outerjoin(models.Vote, models.Vote.post_id == models.Post.id)
        .filter(models.Post.title.contains(search))
        .group_by(models.Post.id)
        .limit(limit)
        .offset(skip)
        .all()
    )

    # pack into dict
    posts = [{"post": post, "votes": votes} for post, votes in posts]

    return posts


def get_post_by_id(db: Session, id: int):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    return post


def create_post(post: schemas.PostCreate, db: Session, current_user: schemas.UserOut):
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


def delete_post(id: int, db: Session):
    db.query(models.Post).filter(models.Post.id == id).delete(synchronize_session=False)
    db.commit()
    return {"message": "Successfully deleted post!"}


def update_post(id: int, post: schemas.PostCreate, db: Session):
    query = db.query(models.Post).filter(models.Post.id == id)
    query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return query.first()


def create_user(user: schemas.UserCreate, db: Session):
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_users(db: Session):
    users = db.query(models.User).all()
    return users


def get_user_by_id(id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    return user


def get_user_by_email(username: str, db: Session):
    user = db.query(models.User).filter(models.User.email == username).first()
    return user


def get_vote(db: Session, post_id: int, user_id: int):
    vote = (
        db.query(models.Vote)
        .filter(models.Vote.post_id == post_id, models.Vote.user_id == user_id)
        .first()
    )
    return vote


def create_vote(db: Session, post_id: int, user_id: int):
    new_vote = models.Vote(post_id=post_id, user_id=user_id)
    db.add(new_vote)
    db.commit()
    return {"message": "Successfully added vote!"}


def delete_vote(db: Session, post_id: int, user_id: int):
    db.query(models.Vote).filter(
        models.Vote.post_id == post_id, models.Vote.user_id == user_id
    ).delete(synchronize_session=False)
    db.commit()
    return {"message": "Successfully deleted vote!"}
