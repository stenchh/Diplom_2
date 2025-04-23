import pytest
import requests
import random
import string
BASE_URL = "https://stellarburgers.nomoreparties.site/api/"


def generate_random_string(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def get_ingredients():
    response = requests.get(f"{BASE_URL}ingredients")
    assert response.status_code == 200
    return response.json()["data"]

@pytest.fixture
def create_user():
    email = f"{generate_random_string}@yandex.ru"
    password = "password"
    name = generate_random_string

    payload = {
        "email": email,
        "password": password,
        "name": name
    }

    response = requests.post(
        'https://your-api-endpoint.ru/api/auth/register',
        json=payload
    )

    user_data = []
    if response.status_code == 201:
        user_data.append(email)
        user_data.append(password)
        user_data.append(name)
        user_data.append(response.json().get('id'))

    return user_data

@pytest.fixture
def registered_user_with_token():
    email = f"{generate_random_string()}@yandex.ru"
    password = "password123"
    name = generate_random_string()

    payload = {
        "email": email,
        "password": password,
        "name": name
    }

    response = requests.post(f"{BASE_URL}auth/register", json=payload)
    assert response.status_code == 200

    tokens = response.json()
    access_token = tokens["accessToken"]

    return {
        "email": email,
        "password": password,
        "name": name,
        "access_token": access_token
    }

@pytest.fixture
def valid_ingredients():
    ingredients = get_ingredients()
    return [ingredients[0]["_id"], ingredients[1]["_id"]]