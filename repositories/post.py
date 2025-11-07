import os
from schema.connection import ENGINE_ASYNC, ENGINE_SYNC
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exc, select, func
from schema import post as post_schema
from fastapi import status
from model.settings import PostStatus, PostVisibility
from model.post import GetPost

async def save(
        body: str, categories: str, comments_allowed: bool,
        embedded_media_url: str | None,
        featured_image_url: str | None,
        post_status: PostStatus, title: str, tags: str | None, user_id: int,
        visibility: PostVisibility
    ) -> int:
    if os.getenv("ENV", "testing") == "prod":
        async with AsyncSession(ENGINE_ASYNC) as session:
            try:
                blog_post = post_schema.BlogPost(
                    body=body,
                    categories=categories,
                    comments_allowed=comments_allowed,
                    embedded_media_url=embedded_media_url,
                    featured_image_url=featured_image_url,
                    status=post_status,
                    title=title,
                    tags=tags,
                    user_id=user_id,
                    visibility=visibility
                )
                session.add(blog_post)
                await session.flush()
                await session.commit()
                return status.HTTP_201_CREATED
            except exc.IntegrityError:
                await session.rollback()
                return status.HTTP_409_CONFLICT
    else:
        with Session(ENGINE_SYNC) as session:
            try:
                blog_post = post_schema.BlogPost(
                    body=body,
                    categories=categories,
                    comments_allowed=comments_allowed,
                    embedded_media_url=embedded_media_url,
                    featured_image_url=featured_image_url,
                    status=post_status,
                    title=title,
                    tags=tags,
                    user_id=user_id,
                    visibility=visibility
                )
                session.add(blog_post)
                session.flush()
                session.commit()
                return status.HTTP_201_CREATED
            except exc.IntegrityError:
                session.rollback()
                return status.HTTP_409_CONFLICT

async def get_post(post_id: int) -> tuple[dict, int]:
    if os.getenv("ENV", "testing") == "prod":
        async with AsyncSession(ENGINE_ASYNC) as session:
            post = await session.get(post_schema.BlogPost, post_id)
            if post:
                return GetPost.model_validate(post).model_dump(by_alias=True), status.HTTP_200_OK
            else:
                return {}, status.HTTP_404_NOT_FOUND
    else:
        with Session(ENGINE_SYNC) as session:
            post = session.get(post_schema.BlogPost, post_id)
            if post:
                return GetPost.model_validate(post).model_dump(by_alias=True), status.HTTP_200_OK
            else:
                return {}, status.HTTP_404_NOT_FOUND

async def get_all_posts(limit: int, offset: int) -> tuple[dict, int]:
    if os.getenv("ENV", "testing") == "prod":
        async with AsyncSession(ENGINE_ASYNC) as session:
            stmt = select(post_schema.BlogPost).order_by(post_schema.BlogPost.id).limit(limit).offset(offset)
            posts = await session.execute(stmt)
            result = posts.scalar().all()

            if len(result) > 0:
                return {"bundle": [GetPost.model_validate(post).model_dump(by_alias=True) for post in result]}, status.HTTP_200_OK
            else:
                return {}, status.HTTP_404_NOT_FOUND
    else:
        with Session(ENGINE_SYNC) as session:
            stmt = select(post_schema.BlogPost).order_by(post_schema.BlogPost.id).limit(limit).offset(offset)
            posts = session.execute(stmt)
            result = posts.scalars().all()

            if len(result) > 0:
                return {"bundle": [GetPost.model_validate(post).model_dump(by_alias=True) for post in result]}, status.HTTP_200_OK
            else:
                return {}, status.HTTP_404_NOT_FOUND

async def get_post_count():
    if os.getenv("ENV", "testing") == "prod":
        async with AsyncSession(ENGINE_ASYNC) as session:
            stmt = select(func.count()).select_from(post_schema.BlogPost)
            count = await session.execute(stmt)
            total_count = count.scalar_one()
            return total_count
    else:
        with Session(ENGINE_SYNC) as session:
            stmt = select(func.count()).select_from(post_schema.BlogPost)
            count = session.execute(stmt)
            total_count = count.scalar_one()
            return total_count

