from pydantic import BaseModel, EmailStr, Field, ConfigDict
from model.settings import Timezones, PrivacySettings, Languages, ProfileTheme

def to_camel(name: str) -> str:
    parts = name.split("_")
    return parts[0] + "".join(word.capitalize() for word in parts[1:])

class UserCreate(BaseModel):
    username: str = Field(min_length=7, max_length=30)
    email: EmailStr
    password: str = Field(min_length=8, max_length=70)
    first_name: str = Field(min_length=1, max_length=50, alias="firstName")
    last_name: str = Field(min_length=1, max_length=50, alias="lastName")
    middle_name: str = Field(min_length=0, max_length=50, alias="middleName")
    timezone: Timezones = Field(default=Timezones.UTC)

class GetUserResponse(BaseModel):
    bio: str = Field(min_length=0, max_length=200)
    email: EmailStr
    first_name: str = Field(min_length=1, max_length=50)
    id: int
    is_active: bool
    last_name: str = Field(min_length=1, max_length=50)
    middle_name: str = Field(min_length=0, max_length=50)
    privacy_settings: PrivacySettings
    profile_language: Languages
    profile_picture_url: str | None
    profile_theme: ProfileTheme
    timezone: Timezones
    username: str = Field(min_length=7, max_length=30)

    model_config = ConfigDict(from_attributes=True, alias_generator=to_camel, populate_by_name=True)
