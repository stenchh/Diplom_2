BASE_URL = "https://stellarburgers.nomoreparties.site/api/"


class TestLoginUser:

    @allure.title("Вход с валидными учетными данными")
    @allure.description("Проверяется, что пользователь может успешно войти в систему с правильными данными.")
    @allure.step("Выполнение входа с правильным email и паролем")
    def test_login_with_valid_credentials(self, create_user):
        payload = {
            "email": create_user["email"],
            "password": create_user["password"]
        }

        response = requests.post(f"{BASE_URL}auth/login", json=payload)
        assert response.status_code == 200

        data = response.json()
        assert data["success"] is True
        assert "accessToken" in data
        assert "refreshToken" in data
        assert data["user"]["email"] == create_user["email"]
        assert data["user"]["name"] == create_user["name"]

    @allure.title("Вход с невалидными учетными данными")
    @allure.description("Проверяется, что при попытке входа с неверными данными возвращается ошибка.")
    @allure.step("Выполнение входа с неправильным email или паролем")
    def test_login_with_invalid_credentials(self):
        payload = {
            "email": "wrongemail@yandex.ru",
            "password": "wrongpassword"
        }

        response = requests.post(f"{BASE_URL}auth/login", json=payload)

        assert response.status_code == 401
        assert response.json()["message"] == "email or password are incorrect"
