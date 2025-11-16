from fastapi import APIRouter, Response, status, Query, Request, Depends
from fastapi.responses import JSONResponse
from model import post
from services import post as post_service
from fastapi.encoders import jsonable_encoder
from security.security import verify_access_token


route = APIRouter(prefix="/posts", tags=["posts"])

@route.post("/")
async def create_post(blog_post: post.CreatePost, current_user = Depends(verify_access_token)) -> Response:
    resp: int = await post_service.create_post(blog_post)
    match resp:
        case status.HTTP_201_CREATED:
            return JSONResponse(content={"message": "post created successfully"}, status_code=resp)
        case _:
            return JSONResponse(content={"message": "error creating post"}, status_code=resp)

@route.get("/")
async def get_post(id: int, current_user = Depends(verify_access_token)) -> Response:
    response, status_code = await post_service.get_post(id)
    match status_code:
        case status.HTTP_200_OK:
            return JSONResponse(content=jsonable_encoder(response), status_code=status_code)
        case _:
            return JSONResponse(content={"message": "post not found"}, status_code=status_code)

@route.get("/all")
async def get_all_posts(
        request: Request, limit: int = Query(gt=0), offset: int = Query(ge=0),
        current_user = Depends(verify_access_token)
):
    response, status_code = await post_service.get_all_posts(limit, offset, request)
    match status_code:
        case status.HTTP_200_OK:
            return JSONResponse(content=jsonable_encoder(response), status_code=status_code)
        case _:
            return JSONResponse(content={"message": "post not found"}, status_code=status_code)