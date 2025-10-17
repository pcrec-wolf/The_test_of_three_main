import unittest
from unittest.mock import patch, call
import io


class TestCoursesTézki(unittest.TestCase):

    def setUp(self):
        self.courses = ["Java-разработчик с нуля", "Fullstack-разработчик на Python", "Python-разработчик с нуля",
                        "Frontend-разработчик с нуля"]
        self.mentors = [
            ["Филипп Воронов", "Анна Юшина", "Иван Бочаров", "Анатолий Корсаков", "Юрий Пеньков", "Илья Сухачев",
             "Иван Маркитан", "Ринат Бибиков", "Вадим Ерошевичев", "Тимур Сейсембаев", "Максим Батырев",
             "Никита Шумский", "Алексей Степанов", "Денис Коротков", "Антон Глушков", "Сергей Индюков",
             "Максим Воронцов", "Евгений Грязнов", "Константин Виролайнен", "Сергей Сердюк", "Павел Дерендяев"],
            ["Евгений Шмаргунов", "Олег Булыгин", "Александр Бардин", "Александр Иванов", "Кирилл Табельский",
             "Александр Ульянцев", "Роман Гордиенко", "Адилет Асканжоев", "Александр Шлейко", "Алена Батицкая",
             "Денис Ежков", "Владимир Чебукин", "Эдгар Нуруллин", "Евгений Шек", "Максим Филипенко", "Елена Никитина"],
            ["Евгений Шмаргунов", "Олег Булыгин", "Дмитрий Демидов", "Кирилл Табельский", "Александр Ульянцев",
             "Александр Бардин", "Александр Иванов", "Антон Солонилин", "Максим Филипенко", "Елена Никитина",
             "Азамат Искаков", "Роман Гордиенко"],
            ["Владимир Чебукин", "Эдгар Нуруллин", "Евгений Шек", "Валерий Хаслер", "Татьяна Тен", "Александр Фитискин",
             "Александр Шлейко", "Алена Батицкая", "Александр Беспоясов", "Денис Ежков", "Николай Лопин",
             "Михаил Ларченко"]
        ]
        self.durations = [14, 20, 12, 20]

        self.courses_list = []
        for course, mentor, duration in zip(self.courses, self.mentors, self.durations):
            course_dict = {"title": course, "mentors": mentor, "duration": duration}
            self.courses_list.append(course_dict)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_find_same_names_output(self, mock_stdout):
        # Запускаем исходный код
        for course in self.courses_list:
            names = [m.split()[0] for m in course["mentors"]]
            unique_names = set(names)

            same_name_list = []
            for name in unique_names:
                if names.count(name) > 1:
                    for mentor in course["mentors"]:
                        if mentor.split()[0] == name:
                            same_name_list.append(mentor)
            same_name_list = sorted(same_name_list)
            if sorted(same_name_list):
                print(f'На курсе {course["title"]} есть тёзки: {", ".join(same_name_list)}')

        output = mock_stdout.getvalue()

        # Проверяем, что вывод содержит ожидаемые строки
        self.assertIn("На курсе Java-разработчик с нуля есть тёзки:", output)
        self.assertIn("На курсе Fullstack-разработчик на Python есть тёзки:", output)
        self.assertIn("На курсе Python-разработчик с нуля есть тёзки:", output)

        # Проверяем конкретные тезки
        self.assertIn("Александр Бардин, Александр Иванов, Александр Ульянцев", output)
        self.assertIn("Александр Бардин, Александр Иванов", output)
        self.assertIn("Евгений Шмаргунов, Евгений Шек", output)

    def test_courses_list_structure(self):
        # Проверяем структуру courses_list
        self.assertEqual(len(self.courses_list), 4)

        for i, course in enumerate(self.courses_list):
            self.assertEqual(course["title"], self.courses[i])
            self.assertEqual(course["mentors"], self.mentors[i])
            self.assertEqual(course["duration"], self.durations[i])

    def test_names_extraction(self):
        # Тестируем извлечение имен из списка менторов
        course = self.courses_list[0]
        names = [m.split()[0] for m in course["mentors"]]

        self.assertEqual(len(names), len(course["mentors"]))
        self.assertIn("Филипп", names)
        self.assertIn("Анна", names)
        self.assertIn("Иван", names)

    def test_unique_names_calculation(self):
        # Тестируем создание множества уникальных имен
        course = self.courses_list[0]
        names = [m.split()[0] for m in course["mentors"]]
        unique_names = set(names)

        self.assertLessEqual(len(unique_names), len(names))
        self.assertTrue(isinstance(unique_names, set))

    def test_same_name_detection(self):
        # Тестируем обнаружение тезок для конкретного курса
        course = self.courses_list[1]  # Fullstack-разработчик на Python
        names = [m.split()[0] for m in course["mentors"]]
        unique_names = set(names)

        same_name_list = []
        for name in unique_names:
            if names.count(name) > 1:
                for mentor in course["mentors"]:
                    if mentor.split()[0] == name:
                        same_name_list.append(mentor)

        same_name_list = sorted(same_name_list)

        # Проверяем, что найдены правильные тезки
        expected_same_names = ["Александр Бардин", "Александр Иванов", "Александр Ульянцев", "Александр Шлейко"]
        found_same_names = [name for name in expected_same_names if name in same_name_list]
        self.assertTrue(len(found_same_names) > 0)

    def test_same_name_list_sorting(self):
        # Тестируем сортировку списка тезок
        test_names = ["Иван Б", "Анна А", "Петр В"]
        sorted_names = sorted(test_names)

        self.assertEqual(sorted_names, ["Анна А", "Иван Б", "Петр В"])

    def test_empty_same_name_list(self):
        # Тестируем случай, когда тезок нет
        empty_course = {
            "title": "Test Course",
            "mentors": ["Иван Иванов", "Петр Петров", "Анна Сидорова"],
            "duration": 10
        }

        names = [m.split()[0] for m in empty_course["mentors"]]
        unique_names = set(names)

        same_name_list = []
        for name in unique_names:
            if names.count(name) > 1:
                for mentor in empty_course["mentors"]:
                    if mentor.split()[0] == name:
                        same_name_list.append(mentor)

        same_name_list = sorted(same_name_list)
        self.assertEqual(same_name_list, [])


if __name__ == '__main__':
    unittest.main()