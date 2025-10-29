import os
from schema.connection import ENGINE_ASYNC, ENGINE_SYNC
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exc
from schema import user as user_schema
from fastapi import status


async def save(
        username: str, email: str, password: str, 
        first_name: str, last_name: str, middle_name: str,
        timezone: str
    ) -> int:
    if os.getenv("ENV", "testing") == "prod":
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


