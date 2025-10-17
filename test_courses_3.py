import unittest


class TestCoursesLogic(unittest.TestCase):

    def setUp(self):
        # Исходные данные
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

        # Создаем courses_list
        self.courses_list = []
        for course, mentor, duration in zip(self.courses, self.mentors, self.durations):
            course_dict = {"title": course, "mentors": mentor, "duration": duration}
            self.courses_list.append(course_dict)

    def test_courses_list_creation(self):
        """Тест создания списка курсов"""
        self.assertEqual(len(self.courses_list), 4)
        self.assertEqual(self.courses_list[0]["title"], "Java-разработчик с нуля")
        self.assertEqual(self.courses_list[1]["duration"], 20)
        self.assertEqual(len(self.courses_list[2]["mentors"]), 12)

    def test_duration_index_calculation(self):
        """Тест расчета индексов по длительности"""
        duration_index = []
        for index, course in enumerate(self.courses_list):
            duration_index.append([course["duration"], index])

        duration_index.sort()

        expected_durations = [[12, 2], [14, 0], [20, 1], [20, 3]]
        self.assertEqual(duration_index, expected_durations)

    def test_mentors_count_index_calculation(self):
        """Тест расчета индексов по количеству менторов"""
        mcount_index = []
        for index, course in enumerate(self.courses_list):
            mcount_index.append([len(course["mentors"]), index])

        mcount_index.sort()

        expected_mentors_count = [[12, 3], [12, 2], [16, 1], [21, 0]]
        self.assertEqual(mcount_index, expected_mentors_count)

    def test_indexes_arrays(self):
        """Тест формирования массивов индексов"""
        # Расчет duration_index
        duration_index = []
        for index, course in enumerate(self.courses_list):
            duration_index.append([course["duration"], index])
        duration_index.sort()

        # Расчет mcount_index
        mcount_index = []
        for index, course in enumerate(self.courses_list):
            mcount_index.append([len(course["mentors"]), index])
        mcount_index.sort()

        # Формирование indexes_d и indexes_m
        indexes_d = []
        indexes_m = []

        for _, idx in duration_index:
            indexes_d.append(idx)
        for _, idx in mcount_index:
            indexes_m.append(idx)

        # Проверяем ожидаемые значения
        self.assertEqual(indexes_d, [2, 0, 1, 3])
        self.assertEqual(indexes_m, [3, 2, 1, 0])

    def test_final_comparison(self):
        """Тест финального сравнения массивов индексов"""
        # Полный расчет как в исходном коде
        duration_index = []
        mcount_index = []
        for index, course in enumerate(self.courses_list):
            duration_index.append([course["duration"], index])
            mcount_index.append([len(course["mentors"]), index])

        duration_index.sort()
        mcount_index.sort()

        indexes_d = []
        indexes_m = []

        for _, idx in duration_index:
            indexes_d.append(idx)
        for _, idx in mcount_index:
            indexes_m.append(idx)

        # Проверяем, что связь отсутствует (как в исходном выводе)
        self.assertNotEqual(indexes_d, indexes_m)
        self.assertEqual(indexes_d, [2, 0, 1, 3])
        self.assertEqual(indexes_m, [3, 2, 1, 0])


if __name__ == '__main__':
    unittest.main()