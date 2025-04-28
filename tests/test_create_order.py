from config import BASE_URL
import allure
import requests



class TestCreateOrder:

    @allure.title("Создание заказа с авторизацией и валидными ингредиентами")
    @allure.description("Проверяется успешное создание заказа при наличии токена и корректных ингредиентов.")
    @allure.step("Отправка запроса на создание заказа с авторизацией и ингредиентами")
    def test_create_order_with_auth_and_ingredients(self, registered_user_with_token, valid_ingredients, delete_user_after_test):
        headers = {
            "Authorization": registered_user_with_token["access_token"]
        }
        payload = {"ingredients": valid_ingredients}

        response = requests.post(f"{BASE_URL}orders", json=payload, headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "order" in data
        assert data["order"]["number"] is not None

    @allure.title("Создание заказа без авторизации")
    @allure.description("Проверяется, что заказ не может быть создан без токена авторизации.")
    @allure.step("Отправка запроса на создание заказа без токена")
    def test_create_order_without_auth(self, valid_ingredients):
        payload = {"ingredients": valid_ingredients}
        response = requests.post(f"{BASE_URL}orders", json=payload)
        assert response.status_code == 401
        data = response.json()
        assert data["success"] is False
        assert data["message"] == "You should should be authorised"


    @allure.title("Создание заказа без ингредиентов")
    @allure.description("Проверяется, что заказ не может быть создан без указания ингредиентов.")
    @allure.step("Отправка запроса с пустым списком ингредиентов")
    def test_create_order_without_ingredients(self, registered_user_with_token, delete_user_after_test):
        headers = {"Authorization": registered_user_with_token["access_token"]}
        payload = {"ingredients": []}

        response = requests.post(f"{BASE_URL}orders", json=payload, headers=headers)
        assert response.status_code == 400
        data = response.json()
        assert data["success"] is False
        assert data["message"] == "Ingredient ids must be provided"

    @allure.title("Создание заказа с невалидными хешами ингредиентов")
    @allure.description("Проверяется, что при передаче некорректных ID ингредиентов возвращается ошибка 500.")
    @allure.step("Отправка запроса с невалидными ID ингредиентов")
    def test_create_order_with_invalid_ingredient_hash(self, registered_user_with_token, delete_user_after_test):
        headers = {"Authorization": registered_user_with_token["access_token"]}
        payload = {"ingredients": ["invalid_hash_1", "invalid_hash_2"]}

        response = requests.post(f"{BASE_URL}orders", json=payload, headers=headers)
        assert response.status_code == 500
