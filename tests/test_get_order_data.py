BASE_URL = "https://stellarburgers.nomoreparties.site/api/"



@allure.step("Получение валидных ингредиентов")
def get_valid_ingredient_ids(count=2):
    response = requests.get(f"{BASE_URL}ingredients")
    assert response.status_code == 200, "Не удалось получить список ингредиентов"

    ingredients = response.json().get("data", [])
    assert ingredients, "Список ингредиентов пуст"

    return [ingredient["_id"] for ingredient in ingredients[:count]]



class TestGetUserOrders:

    @allure.step("Создание заказа с токеном и ингредиентами")
    def create_order(self, token, ingredients):
        headers = {
            "Authorization": token
        }
        payload = {
            "ingredients": ingredients
        }
        response = requests.post(f"{BASE_URL}orders", json=payload, headers=headers)
        assert response.status_code == 200
        return response.json()

    @allure.title("Получение заказов авторизованного пользователя")
    @allure.description("Проверяется, что авторизованный пользователь может получить список своих заказов.")
    def test_get_orders_with_auth(self, registered_user_with_token):
        token = registered_user_with_token["access_token"]
        ingredients = get_valid_ingredient_ids()

        self.create_order(token, ingredients)

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
