from typing import Dict
from fastapi import Depends, APIRouter, status, HTTPException

from sqlalchemy.orm import Session
import os
import sys

curr_dir = os.path.dirname(__name__)
top_dir = os.path.abspath(os.path.join(curr_dir, "../"))
sys.path.insert(0, top_dir)

import models, oauth2, schemas
from database import get_db


router = APIRouter(prefix="/votes", tags=["Vote"])


@router.post("", status_code=status.HTTP_201_CREATED)
def vote(
    body: schemas.VoteCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
) -> Dict:
    """This is used to vote on an existing posts.

    Args:
    -----
    body: The content of the vote. i.e the user input.

    Returns:
    --------
    response: A reponse indicating a vote was successfully added or deleted.
    """
    # verify that post_id exists
    post = db.query(models.Posts).filter(models.Posts.id == body.post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Post:{body.post_id} doesn't exist.",
        )

    query = db.query(models.Votes).filter(
        models.Votes.post_id == body.post_id, models.Votes.user_id == current_user
    )
    query_result = query.first()

    # add vote
    if body.dir == 1:
        if query_result:  # if the user has already voted (liked) the post
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User:{current_user} has already voted.",
            )
        else:
            add_vote = models.Votes(post_id=body.post_id, user_id=current_user)
            db.add(add_vote)
            db.commit()
            return {"Vote successful"}

    # delete vote
    if body.dir < 1:
        if query_result:  # if vote exists in the DB
            query.delete(synchronize_session=False)
            db.commit()
            return {"Vote successfully deleted!"}
        else:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Vote does not exist!",
            )
