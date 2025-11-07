from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from model.settings import PostStatus, PostVisibility, Categories
from model.util import to_camel

class CreatePost(BaseModel):
    body: str = Field(min_length=1, max_length=13000)
    categories: list[Categories]
    comments_allowed: bool = Field(alias="commentsAllowed")
    embedded_media_url: list[str] | None = Field(alias="embeddedMediaUrl")
    featured_image_url: str | None = Field(alias="featuredImageUrl")
    status: PostStatus
    title: str = Field(min_length=1, max_length=100)
    tags: list[str] | None
    user_id: int = Field(alias="userId")
    visibility: PostVisibility

class GetPost(BaseModel):
    body: str = Field(min_length=1, max_length=13000)
    categories: str
    comments_allowed: bool
    date_created: datetime | None
    embedded_media_url: str | None
    featured_image_url: str | None
    last_updated: datetime
    likes: int
    status: PostStatus
    title: str = Field(min_length=1, max_length=100)
    tags: str | None
    user_id: int
    visibility: PostVisibility
    id: int

    model_config = ConfigDict(from_attributes=True, alias_generator=to_camel, populate_by_name=True)





