from conftest import generate_random_string
BASE_URL = "https://stellarburgers.nomoreparties.site/api/"



class TestUpdateUser:

    @allure.title("Изменение данных пользователя с авторизацией")
    @allure.description("Проверяется возможность изменения имени и email при наличии accessToken.")
    @allure.step("Изменение email и имени авторизованного пользователя")
    def test_update_user_with_auth(self, registered_user_with_token):
        headers = {
            "Authorization": registered_user_with_token["access_token"]
        }

        new_email = f"{generate_random_string()}@yandex.ru"
        new_name = generate_random_string()

        payload = {
            "email": new_email,
            "name": new_name
        }

        response = requests.patch(
            f"{BASE_URL}auth/user",
            json=payload,
            headers=headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["user"]["email"] == new_email
        assert data["user"]["name"] == new_name

    @allure.title("Попытка изменения данных без авторизации")
    @allure.description("Проверяется, что при попытке изменить данные без токена возвращается ошибка 401.")
    @allure.step("Запрос на изменение email и имени без токена")
    def test_update_user_without_auth(self):
        payload = {
            "email": f"{generate_random_string()}@yandex.ru",
            "name": generate_random_string()
        }

        response = requests.patch(f"{BASE_URL}auth/user", json=payload)

        assert response.status_code == 401
        data = response.json()
        assert data["message"] == "You should be authorised"
