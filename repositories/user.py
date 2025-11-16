import os
from schema.connection import ENGINE_ASYNC, ENGINE_SYNC
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exc, select, func
from schema import user as user_schema
from fastapi import status
from pydantic import EmailStr
from model.settings import Timezones
from model.user import GetUserResponse


async def save(
        username: str, email: str | EmailStr, password: str,
        first_name: str, last_name: str, middle_name: str,
        timezone: str | Timezones
    ) -> int:
    if os.getenv("POSTFOLIO_ENV", "DEV") == "PROD":
        async with AsyncSession(ENGINE_ASYNC) as session:
            try:
                blog_user = user_schema.BlogUser(
                    email=email,
                    first_name=first_name,
                    is_active=True,
                    last_name=last_name,
                    middle_name=middle_name,
                    privacy_settings=user_schema.PrivacySettings.PUBLIC,
                    profile_language=user_schema.Languages.ENGLISH,
                    profile_picture_url=None,
                    profile_theme=user_schema.ProfileTheme.SYSTEM_DEFAULT,
                    password=password,
                    timezone=timezone,
                    username=username,
                )
                session.add(blog_user)
                await session.flush()
                await session.commit()
                return status.HTTP_201_CREATED
            except exc.IntegrityError:
                await session.rollback()
                return status.HTTP_409_CONFLICT
    else:
        with Session(ENGINE_SYNC) as session:
            try:
                blog_user = user_schema.BlogUser(
                    email=email,
                    first_name=first_name,
                    is_active=True,
                    last_name=last_name,
                    middle_name=middle_name,
                    privacy_settings=user_schema.PrivacySettings.PUBLIC,
                    profile_language=user_schema.Languages.ENGLISH,
                    profile_picture_url=None,
                    profile_theme=user_schema.ProfileTheme.SYSTEM_DEFAULT,
                    password=password,
                    timezone=timezone,
                    username=username,
                )
                session.add(blog_user)
                session.flush()
                session.commit()
                return status.HTTP_201_CREATED
            except exc.IntegrityError:
                session.rollback()
                return status.HTTP_409_CONFLICT

async def get_user(user_id: int) -> tuple[dict, int]:
    if os.getenv("POSTFOLIO_ENV", "DEV") == "PROD":
        async with AsyncSession(ENGINE_ASYNC) as session:
            user = await session.get(user_schema.BlogUser, user_id)
            if user:
                return GetUserResponse.model_validate(user).model_dump(by_alias=True), status.HTTP_200_OK
            else:
                return {}, status.HTTP_404_NOT_FOUND
    else:
        with Session(ENGINE_SYNC) as session:
            user = session.get(user_schema.BlogUser, user_id)
            if user:
                return GetUserResponse.model_validate(user).model_dump(by_alias=True), status.HTTP_200_OK
            else:
                return {}, status.HTTP_404_NOT_FOUND

async def get_all_users(limit: int, offset: int) -> tuple[dict, int]:
    if os.getenv("POSTFOLIO_ENV", "DEV") == "PROD":
        async with AsyncSession(ENGINE_ASYNC) as session:
            stmt = select(user_schema.BlogUser).order_by(user_schema.BlogUser.id).limit(limit).offset(offset)
            users = await session.execute(stmt)
            result = users.scalars().all()
            if len(result) > 0:
                return {"bundle": [GetUserResponse.model_validate(user).model_dump(by_alias=True) for user in result]}, status.HTTP_200_OK
            else:
                return {}, status.HTTP_404_NOT_FOUND
    else:
        with Session(ENGINE_SYNC) as session:
            stmt = select(user_schema.BlogUser).order_by(user_schema.BlogUser.id).limit(limit).offset(offset)
            users = session.execute(stmt)
            result = users.scalars().all()
            if len(result) > 0:
                return {"bundle": [GetUserResponse.model_validate(user).model_dump(by_alias=True) for user in result]}, status.HTTP_200_OK
            else:
                return {}, status.HTTP_404_NOT_FOUND

async def get_user_by_username(username: str) -> tuple[dict, int]:
    if os.getenv("POSTFOLIO_ENV", "DEV") == "PROD":
        async with AsyncSession(ENGINE_ASYNC) as session:
            stmt = select(user_schema.BlogUser).where(user_schema.BlogUser.username == username)
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()
            if user:
                return {
                    "id": user.id,
                    "username": user.username,
                    "password": user.password,
                    "email": user.email,
                    "is_active": user.is_active,
                }, status.HTTP_200_OK
            else:
                return {}, status.HTTP_404_NOT_FOUND
    else:
        with Session(ENGINE_SYNC) as session:
            stmt = select(user_schema.BlogUser).where(user_schema.BlogUser.username == username)
            result = session.execute(stmt)
            user = result.scalar_one_or_none()
            if user:
                return {
                    "id": user.id,
                    "username": user.username,
                    "password": user.password,
                    "email": user.email,
                    "is_active": user.is_active,
                }, status.HTTP_200_OK
            else:
                return {}, status.HTTP_404_NOT_FOUND

async def get_user_count() -> int:
    if os.getenv("POSTFOLIO_ENV", "DEV") == "PROD":
        async with AsyncSession(ENGINE_ASYNC) as session:
            stmt = select(func.count()).select_from(user_schema.BlogUser)
            count = await session.execute(stmt)
            total_count = count.scalar_one()
            return total_count
    else:
        with Session(ENGINE_SYNC) as session:
            stmt = select(func.count()).select_from(user_schema.BlogUser)
            count = session.execute(stmt)
            total_count = count.scalar_one()
            return total_count
