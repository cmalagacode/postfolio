import pytest
import requests
import requests_mock
from app import app
from pydantic import ValidationError
from schema.user import Base
from schema.connection import ENGINE_SYNC
from fastapi.testclient import TestClient
from model.settings import PrivacySettings, ProfileTheme, Languages, Timezones
from model.user import UserCreate
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
    Function tests a valid creation of a user via post request.
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
        "firstName": "J" * 51,
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
        "firstName": "J" * 51,
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
        "lastName": "D" * 51,
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
        "middleName": "D" * 51,
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

