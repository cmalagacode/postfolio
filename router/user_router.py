from fastapi import APIRouter, Response, status, Query, Request
from fastapi.responses import JSONResponse  
from model import user
from services import user as user_service
from fastapi.encoders import jsonable_encoder


route = APIRouter(prefix="/users", tags=["users"])

@route.post("/")
async def create_user(blog_user: user.UserCreate) -> Response:
    resp: int = await user_service.create_user(blog_user)
    match resp:
        case status.HTTP_201_CREATED:
            return JSONResponse(content={"message": "user created successfully"}, status_code=resp)
        case _:
            return JSONResponse(content={"message": "error creating user"}, status_code=resp)

@route.get("/")
async def get_user(id: int) -> Response:
    response, status_code = await user_service.get_user(id)
    match status_code:
        case status.HTTP_200_OK:
            return JSONResponse(content=jsonable_encoder(response), status_code=status_code)
        case _:
            return JSONResponse(content={"message": "user not found"}, status_code=status_code)

@route.get("/all")
async def get_all_users(request: Request, limit: int = Query(gt=0), offset: int = Query(ge=0)):
    response, status_code = await user_service.get_all_users(limit, offset, request)
    match status_code:
        case status.HTTP_200_OK:
            return JSONResponse(content=jsonable_encoder(response), status_code=status_code)
        case _:
            return JSONResponse(content={"message": "user not found"}, status_code=status_code)