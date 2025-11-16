import bcrypt
from repositories import user as user_repo
from security.security import create_access_token
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestFormStrict
from fastapi import status

async def verify_user(credentials: OAuth2PasswordRequestFormStrict) -> dict:
    # get user
    user, status_code = await user_repo.get_user_by_username(credentials.username)
    user_exists = len(user.keys()) > 0
    # compare hashed passwords
    if not user_exists:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    stored_hashed_password = user.get("password")
    if not stored_hashed_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    password_matches = bcrypt.checkpw(
        credentials.password.encode("utf-8"),
        stored_hashed_password.encode("utf-8"),
    )
    if not password_matches:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}
