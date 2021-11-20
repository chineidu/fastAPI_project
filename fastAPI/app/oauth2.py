from typing import Dict, Optional
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm.session import Session
from database import get_db
import schemas
import models
from config import settings

# endpoint for logging users in. It automatically logs the user in.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# load the database credentials.
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRATION_MINUTES = settings.ACCESS_TOKEN_EXPIRATION_MINUTES


def create_access_token(data: Dict, expires_delta: Optional[timedelta] = None) -> str:
    """This is used to create an access token for the user.

    Args:
    -----
    data: The payload.
    expires_delta: The expiration time in minutes.

    Returns:
    --------
    jwt_access_token: The newly created user access token.
    """
    payload_to_encode = data.copy()  # create a copy
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRATION_MINUTES)

    payload_to_encode.update({"exp": expire})  # update the payload

    # create access token
    jwt_access_token = jwt.encode(
        payload_to_encode, key=SECRET_KEY, algorithm=ALGORITHM
    )
    return jwt_access_token


def verify_access_token(
    access_token: str, credentials_exception: str
) -> schemas.TokenData:
    """This is used to verify the access token obtained from the user.

    Args:
    -----
    access_token: The access token to be verified.

    Returns:
    --------
    token_data: The payload extracted from the access token.
    """
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")  # extract the id
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)  # validate the payload
    except JWTError:
        raise credentials_exception
    return token_data


def get_current_user(
    access_token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    """This is used to verify the access token and automatically log a user in.

    Args:
    -----
    access_token: The access token which must be used before a user can login.

    Returns:
    --------
    user_id: The ID of the logged in user.
    """
    credentials_exception: str = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials!",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = verify_access_token(access_token, credentials_exception)
    query_result = db.query(models.Users).filter(models.Users.id == payload.id).first()

    if not query_result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect user_id!"
        )
    user_id = query_result.id
    return user_id
