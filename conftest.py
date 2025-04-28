import pytest
import requests
from helpers.generators import generate_random_string
from helpers.utils import get_ingredients
from config import BASE_URL





@pytest.fixture
def create_user():
    email = f"{generate_random_string()}@yandex.ru"
    password = "password"
    name = generate_random_string()

    payload = {
        "email": email,
        "password": password,
        "name": name
    }

    response = requests.post(
        f'{BASE_URL}auth/register',
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


@pytest.fixture
def delete_user_after_test():
    def _delete_user(user_id):
        delete_response = requests.delete(f"{BASE_URL}/auth/user/{user_id}")
        assert delete_response.status_code == 200

    yield _delete_user