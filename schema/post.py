from datetime import datetime, timezone

from sqlalchemy import Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped
from model.settings import PostStatus, PostVisibility
from sqlalchemy import Enum as SqlEnum
from schema.base import Base

class BlogPost(Base):
    __tablename__ = "blog_post"
    body: Mapped[str] = mapped_column(Text, nullable=False)
    categories: Mapped[str] = mapped_column(Text, nullable=False)
    comments_allowed: Mapped[bool] = mapped_column(Boolean, nullable=False)
    date_created: Mapped[DateTime] = mapped_column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    embedded_media_url: Mapped[str] = mapped_column(Text, nullable=True)
    featured_image_url: Mapped[str] = mapped_column(Text, nullable=True)
    last_updated: Mapped[DateTime] = mapped_column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    likes: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    status: Mapped[PostStatus] = mapped_column(SqlEnum(PostStatus), nullable=False)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    tags: Mapped[str] = mapped_column(Text, nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("blog_user.id"), nullable=False)
    visibility: Mapped[PostVisibility] = mapped_column(SqlEnum(PostVisibility), nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)