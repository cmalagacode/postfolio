from enum import Enum


class PrivacySettings(Enum):
    PUBLIC = "PUBLIC"
    PRIVATE = "PRIVATE"
    FRIENDS_ONLY = "FRIENDS_ONLY"

class ProfileTheme(Enum):
    LIGHT = "LIGHT"
    DARK = "DARK"
    SYSTEM_DEFAULT = "SYSTEM_DEFAULT"

class Languages(Enum):
    ENGLISH = "en"
    SPANISH = "es"
    FRENCH = "fr"
    GERMAN = "de"
    CHINESE = "zh"
    JAPANESE = "ja"
    HINDI = "hi"
    ARABIC = "ar"
    RUSSIAN = "ru"
    PORTUGUESE = "pt"

class Timezones(Enum):
    EST = "EST"
    PST = "PST"
    CST = "CST"
    MST = "MST"
    AKST = "AKST"
    HST = "HST"
    UTC = "UTC"

class PostStatus(Enum):
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"
    DELETED = "DELETED"

class PostVisibility(Enum):
    PUBLIC = "PUBLIC"
    PRIVATE = "PRIVATE"
    FRIENDS_ONLY = "FRIENDS_ONLY"

class Categories(Enum):
    AUTOMOTIVE = "AUTOMOTIVE"
    PERSONAL_DEVELOPMENT = "PERSONAL_DEVELOPMENT"
    LIFE = "LIFE"
    MUSIC = "MUSIC"
    SCIENCE = "SCIENCE"
    TECHNOLOGY = "TECHNOLOGY"
    ART = "ART"
    CULTURE = "CULTURE"
    SPORTS = "SPORTS"
    HEALTH_WELLNESS = "HEALTH_WELLNESS"
    FITNESS = "FITNESS"
    NUTRITION = "NUTRITION"
    TRAVEL = "TRAVEL"
    FOOD = "FOOD"
    POLITICS = "POLITICS"
    EDUCATION = "EDUCATION"
    ENTERTAINMENT = "ENTERTAINMENT"
    GAMING = "GAMING"
    REAL_ESTATE = "REAL_ESTATE"
    FINANCE = "FINANCE"
    OTHER = "OTHER"