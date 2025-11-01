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

async def get_user(user_id: int):
    return await user_repo.get_user(user_id)