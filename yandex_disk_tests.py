import requests
import unittest
import os
from typing import Dict, Any

import configparser
config = configparser.ConfigParser()
config.read('ini.ini')
token = config['tokens']['Ya_token']


class YandexDiskAPITest(unittest.TestCase):
    """
    Тесты для Яндекс.Диск REST API - создание папки
    """

    # Конфигурация
    BASE_URL = "https://cloud-api.yandex.net/v1/disk/resources"
    TOKEN = token
    TEST_FOLDER = "test_folder_api"

    def setUp(self):
        """Настройка перед каждым тестом"""
        if not self.TOKEN:
            self.skipTest("YANDEX_DISK_TOKEN не установлен")

        self.headers = {
            "Authorization": f"OAuth {self.TOKEN}",
            "Content-Type": "application/json"
        }

        # Очистка тестовой папки перед тестами
        try:
            requests.delete(
                f"{self.BASE_URL}?path={self.TEST_FOLDER}",
                headers=self.headers
            )
        except requests.RequestException:
            pass

    def tearDown(self):
        """Очистка после каждого теста"""
        try:
            requests.delete(
                f"{self.BASE_URL}?path={self.TEST_FOLDER}",
                headers=self.headers
            )
        except requests.RequestException:
            pass

    def test_01_create_folder_success(self):
        """Позитивный тест: успешное создание папки"""
        # Создаем папку
        response = requests.put(
            f"{self.BASE_URL}?path={self.TEST_FOLDER}",
            headers=self.headers
        )

        # Проверяем код ответа
        self.assertEqual(response.status_code, 201,
                         f"Ожидался код 201, получен {response.status_code}")

        # Проверяем, что папка появилась в списке файлов
        list_response = requests.get(
            f"{self.BASE_URL}?path=/",
            headers=self.headers
        )

        self.assertEqual(list_response.status_code, 200)

        # Ищем созданную папку в списке
        items = list_response.json().get("_embedded", {}).get("items", [])
        folder_names = [item["name"] for item in items if item["type"] == "dir"]

        self.assertIn(self.TEST_FOLDER, folder_names,
                      f"Папка {self.TEST_FOLDER} не найдена в списке файлов")

        # Проверяем структуру успешного ответа
        success_response = response.json()
        self.assertIn("href", success_response)
        self.assertIn("method", success_response)
        self.assertEqual(success_response["method"], "GET")

    def test_02_create_folder_already_exists(self):
        """Негативный тест: попытка создать папку, которая уже существует"""
        # Сначала создаем папку
        requests.put(
            f"{self.BASE_URL}?path={self.TEST_FOLDER}",
            headers=self.headers
        )

        # Пытаемся создать снова
        response = requests.put(
            f"{self.BASE_URL}?path={self.TEST_FOLDER}",
            headers=self.headers
        )

        # Должна быть ошибка 409 Conflict
        self.assertEqual(response.status_code, 409,
                         f"Ожидалась ошибка 409, получен {response.status_code}")

        # Проверяем структуру ответа с ошибкой
        error_response = response.json()
        self.assertIn("message", error_response)
        self.assertIn("description", error_response)
        self.assertIn("error", error_response)
        self.assertEqual(error_response["error"], "DiskPathPointsToExistentDirectoryError")

    def test_03_create_folder_unauthorized(self):
        """Негативный тест: неавторизованный запрос"""
        response = requests.put(
            f"{self.BASE_URL}?path={self.TEST_FOLDER}",
            headers={"Authorization": "OAuth invalid_token"}
        )

        self.assertEqual(response.status_code, 401,
                         f"Ожидалась ошибка 401, получен {response.status_code}")

        error_response = response.json()
        self.assertEqual(error_response["error"], "UnauthorizedError")

    def test_04_create_folder_invalid_path(self):
        """Негативный тест: неверный путь"""
        invalid_path = "invalid//path//folder"

        response = requests.put(
            f"{self.BASE_URL}?path={invalid_path}",
            headers=self.headers
        )

        self.assertIn(response.status_code, [400, 404],
                      f"Ожидалась ошибка 400 или 404, получен {response.status_code}")

    def test_05_create_folder_nested_success(self):
        """Позитивный тест: создание вложенной папки"""

        # 1. СНАЧАЛА создаем родительскую папку
        parent_response = requests.put(
            f"{self.BASE_URL}?path={self.TEST_FOLDER}",
            headers=self.headers
        )
        self.assertEqual(parent_response.status_code, 201,
                         "Не удалось создать родительскую папку")

        # 2. ПОТОМ создаем вложенную папку
        nested_folder = f"{self.TEST_FOLDER}/nested_subfolder"
        response = requests.put(
            f"{self.BASE_URL}?path={nested_folder}",
            headers=self.headers
        )

        self.assertEqual(response.status_code, 201,
                         f"Ожидался код 201, получен {response.status_code}")

        # 3. Проверяем, что вложенная папка создалась
        list_response = requests.get(
            f"{self.BASE_URL}?path={self.TEST_FOLDER}",
            headers=self.headers
        )

        self.assertEqual(list_response.status_code, 200)

        items = list_response.json().get("_embedded", {}).get("items", [])
        folder_names = [item["name"] for item in items if item["type"] == "dir"]

        self.assertIn("nested_subfolder", folder_names,
                      "Вложенная папка не найдена")

    def test_06_create_folder_without_authentication(self):
        """Негативный тест: запрос без аутентификации"""
        response = requests.put(
            f"{self.BASE_URL}?path={self.TEST_FOLDER}"
            # Без headers
        )

        self.assertEqual(response.status_code, 401,
                         f"Ожидалась ошибка 401, получен {response.status_code}")

    def test_07_create_folder_empty_name(self):
        """Негативный тест: пустое имя папки"""
        response = requests.put(
            f"{self.BASE_URL}?path=",
            headers=self.headers
        )

        self.assertIn(response.status_code, [400, 404],
                      f"Ожидалась ошибка 400 или 404, получен {response.status_code}")


class YandexDiskAPITestAdvanced(unittest.TestCase):
    """Расширенные тесты для Яндекс.Диск API"""

    BASE_URL = "https://cloud-api.yandex.net/v1/disk/resources"
    TOKEN = token

    def setUp(self):
        if not self.TOKEN:
            self.skipTest("YANDEX_DISK_TOKEN не установлен")

        self.headers = {
            "Authorization": f"OAuth {self.TOKEN}",
            "Content-Type": "application/json"
        }

    def test_folder_metadata_after_creation(self):
        """Тест метаданных после создания папки"""
        test_folder = "test_metadata_folder"

        # Создаем папку
        create_response = requests.put(
            f"{self.BASE_URL}?path={test_folder}",
            headers=self.headers
        )

        self.assertEqual(create_response.status_code, 201)

        # Получаем метаданные папки
        meta_response = requests.get(
            f"{self.BASE_URL}?path={test_folder}",
            headers=self.headers
        )

        self.assertEqual(meta_response.status_code, 200)

        metadata = meta_response.json()

        # Проверяем основные поля метаданных
        self.assertEqual(metadata["name"], test_folder)
        self.assertEqual(metadata["type"], "dir")
        self.assertIn("created", metadata)
        self.assertIn("modified", metadata)
        self.assertIn("path", metadata)

        # Очистка
        requests.delete(f"{self.BASE_URL}?path={test_folder}", headers=self.headers)

    def test_concurrent_folder_creation(self):
        """Тест на конкурентное создание папок"""
        import threading

        results = []

        def create_folder(folder_name):
            try:
                response = requests.put(
                    f"{self.BASE_URL}?path={folder_name}",
                    headers=self.headers
                )
                results.append((folder_name, response.status_code))
            except Exception as e:
                results.append((folder_name, str(e)))

        # Создаем несколько папок параллельно
        threads = []
        for i in range(3):
            folder_name = f"concurrent_test_{i}"
            thread = threading.Thread(target=create_folder, args=(folder_name,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        # Проверяем результаты
        success_count = sum(1 for _, code in results if code == 201)
        self.assertGreaterEqual(success_count, 1,
                                "Хотя бы одна папка должна была создаться успешно")

        # Очистка
        for i in range(3):
            folder_name = f"concurrent_test_{i}"
            requests.delete(f"{self.BASE_URL}?path={folder_name}", headers=self.headers)


# Вспомогательные функции
def check_yandex_disk_availability(token: str) -> bool:
    """Проверяет доступность Яндекс.Диск API"""
    try:
        response = requests.get(
            "https://cloud-api.yandex.net/v1/disk/",
            headers={"Authorization": f"OAuth {token}"},
            timeout=10
        )
        return response.status_code == 200
    except requests.RequestException:
        return False


def setup_test_environment():
    """Настройка тестового окружения"""
    TOKEN = token
    if not TOKEN:
        print("Предупреждение: YANDEX_DISK_TOKEN не установлен")
        print("Установите токен: export YANDEX_DISK_TOKEN=your_token")
        return False

    if not check_yandex_disk_availability(TOKEN):
        print("Яндекс.Диск API недоступен")
        return False

    print("Яндекс.Диск API доступен")
    return True


if __name__ == "__main__":
    # Настройка окружения
    if setup_test_environment():
        # Запуск тестов
        unittest.main(verbosity=2)