from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Dict
from database import get_db
import models, schemas, utils, oauth2


router = APIRouter(prefix="/login", tags=["Authentication"])


@router.post("", status_code=status.HTTP_200_OK, response_model=schemas.TokenResponse)
def authenticate_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> Dict:
    """This is used to authenticate the user.

    Args:
    -----
    form_data: The user credentials.

    Returns:
    --------
    login_cred: The login credentials.
    Example:
    --------
    body = {
        "username": "some username",  # "username" is the default key
        "password": "some password"
    }
    """
    # attempt by the user to login
    my_query = db.query(models.Users).filter(models.Users.email == form_data.username)

    query_result = my_query.first()
    if not query_result:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Invalid credentials!",
        )

    # verify the password
    if not utils.verify_password(form_data.password, query_result.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Invalid credentials!",
        )

    payload = {"user_id": query_result.id}
    # create tokem
    jwt_access_token = oauth2.create_access_token(data=payload)
    login_cred = {"access_token": jwt_access_token, "token_type": "bearer"}

    return login_cred
