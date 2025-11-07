import pytest
import requests
import requests_mock
from app import app
from pydantic import ValidationError
from schema.user import Base
from schema.connection import ENGINE_SYNC
from fastapi.testclient import TestClient
from model.settings import PrivacySettings, ProfileTheme, Languages, Timezones
from model.user import UserCreate, GetUserResponse
from schema.database import initialize_database

client = TestClient(app)

@pytest.fixture()
def setup_db():
    Base.metadata.drop_all(bind=ENGINE_SYNC)
    initialize_database()

# request validation in fastapi TestClient
def test_create_user_endpoint(setup_db):
    """
    Function tests user creation via fastapi TestClient.
    """
    resp = client.post("/users", json={
        "username": "example",
        "email": "example@example.com",
        "password": "password",
        "firstName": "John",
        "lastName": "Doe",
        "middleName": "D",
        "timezone": "EST"
    })
    assert resp.status_code == 201
    assert resp.json()["message"] == "user created successfully"

    resp = client.post("/users", json={
        "username": "example",
        "email": "example@example.com",
        "password": "password",
        "firstName": "John",
        "lastName": "Doe",
        "middleName": "D",
        "timezone": "EST"
    })

    assert resp.status_code == 409
    assert resp.json()["message"] == "error creating user"

def test_get_user_endpoint(setup_db):
    """
    Function tests user creation and getting user via fastapi TestClient.
    """
    post_resp = client.post("/users", json={
        "username": "example",
        "email": "example@example.com",
        "password": "password",
        "firstName": "John",
        "lastName": "Doe",
        "middleName": "D",
        "timezone": "EST"
    })

    assert post_resp.status_code == 201

    get_all_user_resp = client.get("/users/all", params={
        "limit": 1,
        "offset": 0
    })

    assert get_all_user_resp.status_code == 200

    get_user_resp = client.get("/users", params={
        "id": get_all_user_resp.json()["bundle"][0]["id"]
    })

    assert get_user_resp.status_code == 200

def test_create_post(setup_db):
    """
    Function tests post creation via fastapi TestClient.
    """
    create_post_resp = client.post("/posts", json={
        "body": "Test Post",
        "categories": ["NUTRITION", "FITNESS", "FOOD"],
        "commentsAllowed": True,
        "embeddedMediaUrl": ["s3://example-bucket/example.mp4"],
        "featuredImageUrl": "s3://example-bucket/example.png",
        "status": "DRAFT",
        "title": "Test Title",
        "tags": ["#food", "#nutrition", "#fitness"],
        "userId": 1,
        "visibility": "PRIVATE"
    })

    assert create_post_resp.status_code == 201
    assert create_post_resp.json()["message"] == "post created successfully"

# settings tests
def test_enum():
    """
    Test enum class members are instances of class
    """
    assert isinstance(PrivacySettings.PUBLIC, PrivacySettings)
    assert isinstance(PrivacySettings.PRIVATE, PrivacySettings)
    assert isinstance(PrivacySettings.FRIENDS_ONLY, PrivacySettings)
    assert isinstance(ProfileTheme.LIGHT, ProfileTheme)
    assert isinstance(ProfileTheme.DARK, ProfileTheme)
    assert isinstance(ProfileTheme.SYSTEM_DEFAULT, ProfileTheme)
    assert isinstance(Languages.ENGLISH, Languages)
    assert isinstance(Languages.SPANISH, Languages)
    assert isinstance(Languages.FRENCH, Languages)
    assert isinstance(Languages.GERMAN, Languages)
    assert isinstance(Languages.CHINESE, Languages)
    assert isinstance(Languages.JAPANESE, Languages)
    assert isinstance(Languages.HINDI, Languages)
    assert isinstance(Languages.ARABIC, Languages)
    assert isinstance(Languages.RUSSIAN, Languages)
    assert isinstance(Languages.PORTUGUESE, Languages)
    assert isinstance(Timezones.EST, Timezones)
    assert isinstance(Timezones.PST, Timezones)
    assert isinstance(Timezones.CST, Timezones)
    assert isinstance(Timezones.MST, Timezones)
    assert isinstance(Timezones.AKST, Timezones)
    assert isinstance(Timezones.HST, Timezones)
    assert isinstance(Timezones.UTC, Timezones)

# mock tests
def create_blog_user_mock(post_body: dict):
    """
    Function is used inside of mock validation tests. 
    The mocker will intercept this request and mock the response.
    """
    response = requests.post('http://localhost:8080/users', json=post_body)
    return response.json()

def test_mock_user_create_validation():
    """
    Function tests user creation via post request. Uses the create_blog_user_mock function.
    request_mock simiulates the interaction.
    """
    post_body = {
        "username": "example",
        "email": "example@example.com",
        "password": "password",
        "firstName": "John",
        "lastName": "Doe",
        "middleName": "D",
        "timezone": "EST"
    }

    # First mock: successful creation
    expected_normal_response = {"message": "user created successfully"}
    with requests_mock.Mocker() as mock:
        mock_post = mock.post('http://localhost:8080/users', json=expected_normal_response, status_code=201)
        response = create_blog_user_mock(post_body)

        assert mock_post.called
        assert mock_post.last_request.json() == post_body
        assert response == expected_normal_response

    # Second mock: duplicate user error
    expected_duplicate_response = {"message": "error creating user"}
    with requests_mock.Mocker() as mock:
        mock_post = mock.post('http://localhost:8080/users', json=expected_duplicate_response, status_code=409)
        response = create_blog_user_mock(post_body)

        assert mock_post.called
        assert mock_post.last_request.json() == post_body
        assert response == expected_duplicate_response

# pydantics tests
def test_pydantics_create_user_valid():
    """
    Function tests pydantics model for create user.
    """
    data = {
        "username": "example",
        "email": "example@example.com",
        "password": "password",
        "firstName": "John",
        "lastName": "Doe",
        "middleName": "D",
        "timezone": "EST"
    }
    user = UserCreate(**data)
    assert user.username == "example"
    assert user.email == "example@example.com"

def test_pydantics_create_user_invalid_email():
    """
    Function tests if response is pydantics ValidationError to invalid email input.
    """
    test1 = {
        "username": "example",
        "email": "exampleexample.com",
        "password": "password",
        "firstName": "John",
        "lastName": "Doe",
        "middleName": "D",
        "timezone": "EST"
    }

    with pytest.raises(ValidationError):
        UserCreate(**test1)

    test2 = {
        "username": "example",
        "email": "example.com",
        "password": "password",
        "firstName": "John",
        "lastName": "Doe",
        "middleName": "D",
        "timezone": "EST"
    }

    with pytest.raises(ValidationError):
        UserCreate(**test2)

    test3 = {
        "username": "example",
        "email": "",
        "password": "password",
        "firstName": "John",
        "lastName": "Doe",
        "middleName": "D",
        "timezone": "EST"
    }

    with pytest.raises(ValidationError):
        UserCreate(**test3)

def test_pydantics_create_user_invalid_password():
    """
    Function tests if response is pydantics ValidationError to invalid password input.
    """
    test1 = { 
        "username": "example",
        "email": "example@example.com",
        "password": "passwor",
        "firstName": "John",
        "lastName": "Doe",
        "middleName": "D",
        "timezone": "EST"
    }

    with pytest.raises(ValidationError):
        UserCreate(**test1)

    test2 = { 
        "username": "example",
        "email": "example@example.com",
        "password": "passwo",
        "firstName": "John",
        "lastName": "Doe",
        "middleName": "D",
        "timezone": "EST"
    }

    with pytest.raises(ValidationError):
        UserCreate(**test2)

    test3 = { 
        "username": "example",
        "email": "example@example.com",
        "password": "",
        "firstName": "John",
        "lastName": "Doe",
        "middleName": "D",
        "timezone": "EST"
    }

    with pytest.raises(ValidationError):
        UserCreate(**test3)

def test_pydantics_create_user_invalid_username():
    """
    Function tests if response is pydantics ValidationError to invalid username input.
    """
    test1 = {
        "username": "",
        "email": "example@example.com",
        "password": "password",
        "firstName": "J",
        "lastName": "D",
        "middleName": "D",
        "timezone": "EST"
    }

    with pytest.raises(ValidationError):
        UserCreate(**test1)

    test2 = {
        "username": "e" * 31,
        "email": "example@example.com",
        "password": "password",
        "firstName": "",
        "lastName": "",
        "middleName": "D",
        "timezone": "EST"
    }

    with pytest.raises(ValidationError):
        UserCreate(**test2)

def test_pydantics_create_user_invalid_firstname():
    """
    Function tests if response is pydantics ValidationError to invalid firstname input.
    """
    test1 = {
        "username": "example",
        "email": "example@example.com",
        "password": "password",
        "firstName": "J" * 101,
        "lastName": "D",
        "middleName": "D",
        "timezone": "EST"
    }

    with pytest.raises(ValidationError):
        UserCreate(**test1)

    test2 = {
        "username": "example",
        "email": "example@example.com",
        "password": "password",
        "firstName": "",
        "lastName": "",
        "middleName": "D",
        "timezone": "EST"
    }

    with pytest.raises(ValidationError):
        UserCreate(**test2)

def test_pydantics_create_user_invalid_lastname():
    """
    Function tests if response is pydantics ValidationError to invalid lastname input.
    """
    test1 = {
        "username": "example",
        "email": "example@example.com",
        "password": "password",
        "firstName": "John",
        "lastName": "D" * 101,
        "middleName": "D",
        "timezone": "EST"
    }

    with pytest.raises(ValidationError):
        UserCreate(**test1)

    test2 = {
        "username": "example",
        "email": "example@example.com",
        "password": "password",
        "firstName": "John",
        "lastName": "",
        "middleName": "D",
        "timezone": "EST"
    }

    with pytest.raises(ValidationError):
        UserCreate(**test2)


def test_pydantics_create_user_invalid_middlename():
    """
    Function tests if response is pydantics ValidationError to invalid middlename input.
    """
    test1 = {
        "username": "example",
        "email": "example@example.com",
        "password": "password",
        "firstName": "John",
        "lastName": "Doe",
        "middleName": "D" * 101,
        "timezone": "EST"
    }

    with pytest.raises(ValidationError):
        UserCreate(**test1)

def test_pydantics_create_user_invalid_timezone():
    """
    Function tests if response is pydantics ValidationError to invalid timezone input.
    """
    test1 = {
        "username": "example",
        "email": "example@example.com",
        "password": "password",
        "firstName": "John",
        "lastName": "Doe",
        "middleName": "D",
        "timezone": "AAP"
    }

    with pytest.raises(ValidationError):
        UserCreate(**test1)

    test2 = {
        "username": "example",
        "email": "example@example.com",
        "password": "password",
        "firstName": "John",
        "lastName": "Doe",
        "middleName": "D",
        "timezone": "EEAA"
    }

    with pytest.raises(ValidationError):
        UserCreate(**test2)

def test_pydantics_get_user_valid():
    """
    Function tests pydantics model for get user.
    """
    bio = "This is an example bio."
    email = "example@email.com"
    first_name = "John"
    id = 1
    is_active = True
    last_name = "Doe"
    middle_name = "D"
    privacy_settings = PrivacySettings.PUBLIC
    profile_language = Languages.ENGLISH
    profile_picture_url = None
    profile_theme = ProfileTheme.SYSTEM_DEFAULT
    timezone = Timezones.EST
    username = "exampleUser"
    data = {
        "bio": bio,
        "email": email,
        "first_name": first_name,
        "id": id,
        "is_active": is_active,
        "last_name": last_name,
        "middle_name": middle_name,
        "privacy_settings": privacy_settings,
        "profile_language": profile_language,
        "profile_picture_url": profile_picture_url,
        "profile_theme": profile_theme,
        "timezone": timezone,
        "username": username
    }

    user = GetUserResponse(**data)
    assert user.bio == bio
    assert user.email == email
    assert user.first_name == first_name
    assert user.id == id
    assert user.is_active == is_active
    assert user.last_name == last_name
    assert user.middle_name == middle_name
    assert user.privacy_settings == privacy_settings
    assert user.profile_language == profile_language
    assert user.profile_picture_url == profile_picture_url
    assert user.profile_theme == profile_theme
    assert user.timezone == timezone
    assert user.username == username

def test_pydantics_get_user_invalid_bio():
    """
    Function tests if pydantic validation error occurs
    """
    bio = "T" * 201
    email = "e@email.com"
    first_name = "J"
    id = 2
    is_active = True
    last_name = "D"
    middle_name = "E"
    privacy_settings = PrivacySettings.FRIENDS_ONLY
    profile_language = Languages.SPANISH
    profile_picture_url = "s3://example-bucket/example-picture.png"
    profile_theme = ProfileTheme.LIGHT
    timezone = Timezones.MST
    username = "example89232"
    data = {
        "bio": bio,
        "email": email,
        "first_name": first_name,
        "id": id,
        "is_active": is_active,
        "last_name": last_name,
        "middle_name": middle_name,
        "privacy_settings": privacy_settings,
        "profile_language": profile_language,
        "profile_picture_url": profile_picture_url,
        "profile_theme": profile_theme,
        "timezone": timezone,
        "username": username
    }
    with pytest.raises(ValidationError):
        GetUserResponse(**data)

def test_pydantics_get_user_invalid_email():
    """
    Function tests if pydantic validation error occurs
    """
    bio = ""
    email = "email.com"
    first_name = "J"
    id = 3
    is_active = True
    last_name = "D"
    middle_name = "E"
    privacy_settings = PrivacySettings.FRIENDS_ONLY
    profile_language = Languages.SPANISH
    profile_picture_url = "s3://example-bucket/example-picture.png"
    profile_theme = ProfileTheme.LIGHT
    timezone = Timezones.MST
    username = "example89232"
    data = {
        "bio": bio,
        "email": email,
        "first_name": first_name,
        "id": id,
        "is_active": is_active,
        "last_name": last_name,
        "middle_name": middle_name,
        "privacy_settings": privacy_settings,
        "profile_language": profile_language,
        "profile_picture_url": profile_picture_url,
        "profile_theme": profile_theme,
        "timezone": timezone,
        "username": username
    }
    with pytest.raises(ValidationError):
        GetUserResponse(**data)

def test_pydantics_get_user_invalid_first_name():
    """
    Function tests if pydantic validation error occurs
    """
    bio = ""
    email = "example@email.com"
    first_name = "J" * 101
    id = 4
    is_active = True
    last_name = "D"
    middle_name = "E"
    privacy_settings = PrivacySettings.FRIENDS_ONLY
    profile_language = Languages.SPANISH
    profile_picture_url = "s3://example-bucket/example-picture.png"
    profile_theme = ProfileTheme.LIGHT
    timezone = Timezones.MST
    username = "example89232"
    data = {
        "bio": bio,
        "email": email,
        "first_name": first_name,
        "id": id,
        "is_active": is_active,
        "last_name": last_name,
        "middle_name": middle_name,
        "privacy_settings": privacy_settings,
        "profile_language": profile_language,
        "profile_picture_url": profile_picture_url,
        "profile_theme": profile_theme,
        "timezone": timezone,
        "username": username
    }
    with pytest.raises(ValidationError):
        GetUserResponse(**data)

def test_pydantics_get_user_invalid_last_name():
    """
    Function tests if pydantic validation error occurs
    """
    bio = ""
    email = "example@email.com"
    first_name = "J"
    id = 5
    is_active = True
    last_name = "D" * 101
    middle_name = "E"
    privacy_settings = PrivacySettings.FRIENDS_ONLY
    profile_language = Languages.SPANISH
    profile_picture_url = "s3://example-bucket/example-picture.png"
    profile_theme = ProfileTheme.LIGHT
    timezone = Timezones.MST
    username = "example89232"
    data = {
        "bio": bio,
        "email": email,
        "first_name": first_name,
        "id": id,
        "is_active": is_active,
        "last_name": last_name,
        "middle_name": middle_name,
        "privacy_settings": privacy_settings,
        "profile_language": profile_language,
        "profile_picture_url": profile_picture_url,
        "profile_theme": profile_theme,
        "timezone": timezone,
        "username": username
    }
    with pytest.raises(ValidationError):
        GetUserResponse(**data)

def test_pydantics_get_user_invalid_middle_name():
    """
    Function tests if pydantic validation error occurs
    """
    bio = ""
    email = "example@email.com"
    first_name = "J"
    id = 6
    is_active = True
    last_name = "D"
    middle_name = "E" * 101
    privacy_settings = PrivacySettings.FRIENDS_ONLY
    profile_language = Languages.SPANISH
    profile_picture_url = "s3://example-bucket/example-picture.png"
    profile_theme = ProfileTheme.LIGHT
    timezone = Timezones.MST
    username = "example89232"
    data = {
        "bio": bio,
        "email": email,
        "first_name": first_name,
        "id": id,
        "is_active": is_active,
        "last_name": last_name,
        "middle_name": middle_name,
        "privacy_settings": privacy_settings,
        "profile_language": profile_language,
        "profile_picture_url": profile_picture_url,
        "profile_theme": profile_theme,
        "timezone": timezone,
        "username": username
    }
    with pytest.raises(ValidationError):
        GetUserResponse(**data)

def test_pydantics_get_user_invalid_username():
    """
    Function tests if pydantic validation error occurs
    """
    bio = ""
    email = "example@email.com"
    first_name = "J"
    id = 7
    is_active = True
    last_name = "D"
    middle_name = "E"
    privacy_settings = PrivacySettings.FRIENDS_ONLY
    profile_language = Languages.SPANISH
    profile_picture_url = "s3://example-bucket/example-picture.png"
    profile_theme = ProfileTheme.LIGHT
    timezone = Timezones.MST
    username = "e" * 31
    data = {
        "bio": bio,
        "email": email,
        "first_name": first_name,
        "id": id,
        "is_active": is_active,
        "last_name": last_name,
        "middle_name": middle_name,
        "privacy_settings": privacy_settings,
        "profile_language": profile_language,
        "profile_picture_url": profile_picture_url,
        "profile_theme": profile_theme,
        "timezone": timezone,
        "username": username
    }
    with pytest.raises(ValidationError):
        GetUserResponse(**data)