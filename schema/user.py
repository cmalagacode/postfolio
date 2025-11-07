from sqlalchemy import Integer, String, Boolean, Text
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import Enum as SqlEnum
from model.settings import PrivacySettings, ProfileTheme, Languages, Timezones
from schema.base import Base

class BlogUser(Base):
    __tablename__ = "blog_user"
    bio: Mapped[str] = mapped_column(String(200), nullable=True, default="")
    email: Mapped[str] = mapped_column(String(254), unique=True, index=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    middle_name: Mapped[str] = mapped_column(String(100), nullable=False)
    privacy_settings: Mapped[PrivacySettings] = mapped_column(SqlEnum(PrivacySettings, native_enum=False), default=PrivacySettings.PUBLIC, nullable=False)
    profile_language: Mapped[Languages] = mapped_column(SqlEnum(Languages, native_enum=False), default=Languages.ENGLISH, nullable=False)
    profile_picture_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    profile_theme: Mapped[ProfileTheme] = mapped_column(SqlEnum(ProfileTheme, native_enum=False), default=ProfileTheme.SYSTEM_DEFAULT, nullable=False)
    password: Mapped[str] = mapped_column(String(60), nullable=False)
    timezone: Mapped[Timezones] = mapped_column(SqlEnum(Timezones, native_enum=False), default=Timezones.UTC, nullable=False)
    username: Mapped[str] = mapped_column(String(30), unique=True, index=True, nullable=False)
