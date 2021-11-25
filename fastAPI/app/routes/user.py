from typing import List, Dict
from fastapi import HTTPException, Response, status, Depends, APIRouter
from sqlalchemy.orm import Session

from database import get_db
import models, schemas, utils, oauth2

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse
)
def create_user(body: schemas.UserCreate, db: Session = Depends(get_db)) -> Dict:
    """This is used to create a new user.

    Args:
    -----
    body: The user details.

    Returns:
    --------
    new_user_info: The newly created user info.
    """
    from sqlalchemy import exc

    try:
        # hash the user password
        hashed_pswd = utils.hash_password(body.password)
        # update the password
        body.password = hashed_pswd
        new_user_info = models.Users(**body.dict())
        db.add(new_user_info)
        db.commit()
        return new_user_info

    except exc.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=f"The email: {body.email} is already taken. Try another email.",
        )


@router.get("/{id}", response_model=schemas.UserResponse)
def get_user_by_id(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
) -> Dict:
    """This is used to get the basic information of a specific user using the user id.

    Args:
    -----
    id: The user id.

    Returns:
    --------
    new_user_info: The newly created user info.
    """
    my_query = db.query(models.Users).filter(models.Users.id == id)
    query_result = my_query.first()

    if not query_result:
        utils.error_msg(id)

    return query_result


@router.get("", response_model=List[schemas.UserResponse])
def get_all_users(
    db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)
):
    """This is used to get the basic information of all users.

    Args:
    -----

    Returns:
    --------
    all_users_info: The newly created user info.
    """
    my_query_result = db.query(models.Users).all()
    return my_query_result
