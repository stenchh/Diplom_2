from config import BASE_URL
from helpers.utils import get_valid_ingredient_ids
from helpers.utils import create_order
import requests
import allure




class TestGetUserOrders:

    @allure.title("Получение заказов авторизованного пользователя")
    @allure.description("Проверяется, что авторизованный пользователь может получить список своих заказов.")
    def test_get_orders_with_auth(self, registered_user_with_token):
        token = registered_user_with_token["access_token"]
        ingredients = get_valid_ingredient_ids()

        create_order(token, ingredients)

        headers = {
            "Authorization": token
        }
        response = requests.get(f"{BASE_URL}orders", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "orders" in data
        assert isinstance(data["orders"], list)
        assert len(data["orders"]) > 0

    @allure.title("Получение заказов без авторизации")
    @allure.description("Проверяется, что при попытке получить заказы без авторизации возвращается 401.")
    def test_get_orders_without_auth(self):
        response = requests.get(f"{BASE_URL}orders")
        assert response.status_code == 401
        data = response.json()
        assert data["success"] is False
        assert data["message"] == "You should be authorised"
