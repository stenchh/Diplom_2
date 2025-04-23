import random
import string


BASE_URL = "https://stellarburgers.nomoreparties.site/api/"


class TestCreateUser:

    @allure.title("Создание пользователя с валидными данными")
    @allure.description("Проверяется, что пользователь может быть успешно создан, если переданы все необходимые поля.")
    @allure.step("Генерация случайного email и имени")
    def generate_random_string(self, length):
        return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

    @allure.step("Отправка запроса на регистрацию с валидными данными")
    def test_create_user_with_full_data_only(self):
        payload = {
            "email": f"{self.generate_random_string(10)}@yandex.ru",
            "password": "password123",
            "name": self.generate_random_string(10)
        }

        response = requests.post(f'{BASE_URL}auth/register', json=payload)
        assert response.status_code == 200

    @allure.title("Создание пользователя без email")
    @allure.description("Проверяется, что регистрация не проходит, если не передан email.")
    @allure.step("Отправка запроса с пустым email")
    def test_create_user_without_email(self):
        payload = {
            "email": "",
            "password": "password123",
            "name": "Username"
        }

        response = requests.post(f'{BASE_URL}auth/register', json=payload)
        assert response.status_code == 403
        assert response.json() == {'message': 'Email, password and name are required fields', 'success': False}

    @allure.title("Создание пользователя без пароля")
    @allure.description("Проверяется, что регистрация не проходит, если не передан пароль.")
    @allure.step("Отправка запроса с пустым паролем")
    def test_create_user_without_password(self):
        payload = {
            "email": "test@yandex.ru",
            "password": "",
            "name": "Username"
        }

        response = requests.post(f'{BASE_URL}auth/register', json=payload)
        assert response.status_code == 403
        assert response.json() == {'message': 'Email, password and name are required fields', 'success': False}

    @allure.title("Создание пользователя без имени")
    @allure.description("Проверяется, что регистрация не проходит, если не передано имя.")
    @allure.step("Отправка запроса с пустым именем")
    def test_create_user_without_name(self):
        payload = {
            "email": "test@yandex.ru",
            "password": "password123",
            "name": ""
        }

        response = requests.post(f'{BASE_URL}auth/register', json=payload)
        assert response.status_code == 403
        assert response.json() == {'message': 'Email, password and name are required fields', 'success': False}

    @allure.title("Создание дубликата пользователя")
    @allure.description("Проверяется, что невозможно создать пользователя с уже существующим email.")
    @allure.step("Повторная регистрация уже созданного пользователя")
    def test_create_duplicate_user(self, create_user):
        response = requests.post(
            f'{BASE_URL}auth/register',
            json={
                "email": create_user["email"],
                "password": create_user["password"],
                "name": create_user["name"]
            }
        )
        assert response.status_code == 403
        assert response.json() == {'message': 'User already exists', 'success': False}
