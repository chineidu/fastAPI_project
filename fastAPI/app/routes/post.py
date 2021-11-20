from typing import List, Dict, Optional
from fastapi import HTTPException, Response, status, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
import os
import sys

curr_dir = os.path.dirname(__file__)
top_dir = os.path.abspath(os.path.join(curr_dir, ".."))

# insert top_dir into system path
sys.path.insert(0, top_dir)

from database import get_db
import models, schemas, utils, oauth2

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse
)
def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
) -> Dict:
    """This is used to create a new post.

    Args:
    -----
    post: The new post to be created.

    Returns:
    --------
    new_post: The newly created post.
    """
    new_post = models.Posts(
        owner_id=current_user, **post.dict()
    )  # add as key-value pairs
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # used to return the newly created data to the frontend

    return new_post


@router.get("/", response_model=List[schemas.PostResponse2])
def get_posts(
    db: Session = Depends(get_db),
    _: int = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
) -> List[Dict]:
    """This is used to load all the posts in the database.

    Returns:
    --------
    all_posts: All the posts stored in the database.
    """
    # SELECT * FROM posts
    all_posts = (
        db.query(models.Posts, func.count(models.Votes.post_id).label("votes"))
        .join(models.Votes, models.Posts.id == models.Votes.post_id, isouter=True)
        .filter(models.Posts.title.contains(search))
        .group_by(models.Posts.id)
        .order_by(models.Posts.id)
        .limit(limit)
        .offset(skip)
        .all()
    )

    return all_posts  # FastAPI automatically serializes the data.


@router.get("/{id}", response_model=schemas.PostResponse2)
def get_post(
    id: int,
    db: Session = Depends(get_db),
    _: int = Depends(oauth2.get_current_user),
) -> Dict:
    """This is used to retrieve a single post using a unique post id.
    Args:
    -----
    id: The id of the post to be retrieved.

    Returns:
    --------
    query_result: The retrieved post.
    """
    my_query = (
        db.query(models.Posts, func.count(models.Votes.post_id).label("votes"))
        .join(models.Votes, models.Posts.id == models.Votes.post_id, isouter=True)
        .filter(models.Posts.id == id)
        .group_by(models.Posts.id)
    )
    print(my_query)
    query_result = my_query.first()

    if not query_result:
        utils.error_msg(id)

    return query_result


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(
    id: int,
    post: schemas.PostUpdate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
) -> Dict:
    """This is used to update an existing post.

    Args:
    -----
    id: The id of the post to be retrieved.
    post: The new post to be updated.

    Returns:
    --------
    updated_post: The updated post.
    """
    my_query = db.query(models.Posts).filter(models.Posts.id == id)  # query object
    query_result = my_query.first()

    if not query_result:
        utils.error_msg(id)

    # check if the post was made by the user
    if query_result.owner_id != current_user:
        utils.error_msg_2()
    my_query.update(post.dict(), synchronize_session=False)  # update the query object
    db.commit()
    updated_post = my_query.first()
    return updated_post


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
) -> None:
    """This is used to delete an existing post.

    Args:
    -----
    id: The id of the post to be deleted.

    Returns:
    --------
    None
    """
    my_query = db.query(models.Posts).filter(models.Posts.id == id)  # query object
    query_result = my_query.first()

    if not query_result:
        utils.error_msg(id)

    # check if the post was made by the user
    if query_result.owner_id != current_user:
        utils.error_msg_2()
    my_query.delete(synchronize_session=False)  # delete the query object
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
