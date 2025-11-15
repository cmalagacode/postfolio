from fastapi import APIRouter, Response, status, Depends
from fastapi.responses import JSONResponse
from services import login as login_service
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestFormStrict


route = APIRouter(prefix="/login", tags=["login"])

@route.post("/")
async def verify_login(form_data: OAuth2PasswordRequestFormStrict = Depends()) -> Response:
    try:
        token = await login_service.verify_user(form_data)
        return JSONResponse(content=token, status_code=status.HTTP_200_OK)
    except HTTPException:
        return JSONResponse(content={"message": "invalid credentials"}, status_code=status.HTTP_401_UNAUTHORIZED)
