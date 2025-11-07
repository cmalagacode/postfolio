import json
from fastapi import Request
from repositories import post as post_repo
from model import post

async def create_post(post: post.CreatePost) -> int:
    return await post_repo.save(
        body=post.body,
        categories=json.dumps([cat.value for cat in post.categories]),
        comments_allowed=post.comments_allowed,
        embedded_media_url=json.dumps(post.embedded_media_url),
        featured_image_url=post.featured_image_url,
        post_status=post.status,
        title=post.title,
        tags=json.dumps(post.tags),
        user_id=post.user_id,
        visibility=post.visibility
    )

async def get_post(post_id: int) -> tuple[dict, int]:
    return await post_repo.get_post(post_id)

async def get_all_posts(limit: int, offset: int, request: Request) -> tuple[dict, int]:
    response, status_code = await post_repo.get_all_posts(limit, offset)
    total_posts = await post_repo.get_post_count()

    if status_code == 200:
        response["totalCountPosts"] = total_posts
        if limit + offset < total_posts:
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
