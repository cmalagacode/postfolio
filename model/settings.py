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