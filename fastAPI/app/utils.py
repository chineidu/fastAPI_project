from typing import Optional, List, Dict
from fastapi import HTTPException, status
from passlib.context import CryptContext


# for password hashing
pswd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def error_msg(id: int) -> Dict:
    """This is used to display the error message with the HTTP status code.

    Args:
    -----
    id: The id of the post to be retrieved/deleted.

    Returns:
    --------
    It raises an HTTPException
    """
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"The post with id:'{id}' was not found.",
    )


def error_msg_2() -> Dict:
    """This is used to display the error message with the HTTP status code.

    Args:
    -----

    Returns:
    --------
    It raises an HTTPException
    """
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You cannot perform the requested action.",
    )


def hash_password(password: str) -> str:
    """This is used to hash the password.

    Args:
    -----
    password: The actual password

    Returns:
    --------
    hashed_pswd: The hashed password.
    """
    global pswd_context
    hashed_pswd = pswd_context.hash(password)
    return hashed_pswd


def verify_password(login_attempt: str, actual_pswd: str):
    """This is used to verify the user's password.

    Args:
    -----
    login_attempt: The attempted password.
    actual_pswd: The actual password

    Returns:
    --------
    v_resp: The verification rssponse.
    """
    global pswd_context
    v_resp = pswd_context.verify(login_attempt, actual_pswd)
    return v_resp
