from fastapi import Request
import bcrypt
from repositories import user as user_repo
from model import user

async def create_user(user: user.UserCreate) -> int:
    hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt(14)).decode("utf-8")
    return await user_repo.save(
        username=user.username,
        email=user.email,
        password=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
        middle_name=user.middle_name,
        timezone=user.timezone
    )

async def get_user(user_id: int) -> tuple[dict, int]:
    return await user_repo.get_user(user_id)

async def get_all_users(limit: int, offset: int, request: Request):
    response, status_code = await user_repo.get_all_users(limit, offset)
    total_users = await user_repo.get_user_count()

    if status_code == 200:
        response["totalCountUsers"] = total_users
        if limit + offset < total_users:
            next_offset = offset + limit
            response["nextPage"] = str(request.url.include_query_params(limit=limit, offset=next_offset))
        else:
            response["nextPage"] = None


        if offset > 0:
            prev_offset = max(offset - limit, 0)
            response["previousPage"] = str(request.url.include_query_params(limit=limit, offset=prev_offset))
        else:
            response["previousPage"] = None

    return response, status_code