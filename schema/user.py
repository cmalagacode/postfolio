from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import Enum as SqlEnum
from model.settings import PrivacySettings, ProfileTheme, Languages, Timezones

class Base(DeclarativeBase):
    pass

class BlogUser(Base):
    __tablename__ = "blog_user"
    bio: Mapped[str] = mapped_column(String, nullable=True, default="")
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    middle_name: Mapped[str] = mapped_column(String, nullable=False)
    privacy_settings: Mapped[str] = mapped_column(SqlEnum(PrivacySettings, native_enum=False), default=PrivacySettings.PUBLIC, nullable=False)
    profile_language: Mapped[str] = mapped_column(SqlEnum(Languages, native_enum=False), default=Languages.ENGLISH, nullable=False)
    profile_picture_url: Mapped[str | None] = mapped_column(String, nullable=True)
    profile_theme: Mapped[str] = mapped_column(SqlEnum(ProfileTheme, native_enum=False), default=ProfileTheme.SYSTEM_DEFAULT, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    timezone: Mapped[str] = mapped_column(SqlEnum(Timezones, native_enum=False), default=Timezones.UTC, nullable=False)
    username: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)