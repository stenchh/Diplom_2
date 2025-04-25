import requests
from config import BASE_URL
def get_valid_ingredient_ids(count=2):
    response = requests.get(f"{BASE_URL}ingredients")
    assert response.status_code == 200, "Не удалось получить список ингредиентов"

    ingredients = response.json().get("data", [])
    assert ingredients, "Список ингредиентов пуст"

    return [ingredient["_id"] for ingredient in ingredients[:count]]


def create_order(token, ingredients):
    headers = {
        "Authorization": token
    }
    payload = {
        "ingredients": ingredients
    }
    response = requests.post(f"{BASE_URL}orders", json=payload, headers=headers)
    assert response.status_code == 200
    return response.json()


def get_ingredients():
    response = requests.get(f"{BASE_URL}ingredients")
    assert response.status_code == 200
    return response.json()["data"]