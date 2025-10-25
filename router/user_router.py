from fastapi import APIRouter, Response, status
from fastapi.responses import JSONResponse  
from model import user
from services import user as user_service


route = APIRouter(prefix="/users", tags=["users"])

@route.post("/")
async def create_user(user: user.UserCreate) -> Response:
    resp: int = await user_service.create_user(user)
    match resp:
        case status.HTTP_201_CREATED:
            return JSONResponse(content={"message": "user created successfully"}, status_code=resp)
        case _:
            return JSONResponse(content={"message": "error creating user"}, status_code=resp)