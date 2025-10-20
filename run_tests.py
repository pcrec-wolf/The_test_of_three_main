import unittest
import sys
import os

# Добавляем текущую директорию в путь
sys.path.append(os.path.dirname(__file__))

from yandex_disk_tests import YandexDiskAPITest, YandexDiskAPITestAdvanced


def run_specific_tests():
    """Запуск конкретных тестов"""
    test_suite = unittest.TestSuite()

    # Добавляем только нужные тесты
    test_suite.addTest(YandexDiskAPITest('test_01_create_folder_success'))
    test_suite.addTest(YandexDiskAPITest('test_02_create_folder_already_exists'))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)

    return result.wasSuccessful()


if __name__ == "__main__":
    # Запуск всех тестов
    unittest.main(module='yandex_disk_tests', verbosity=2)