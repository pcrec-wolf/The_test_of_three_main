import pytest
from main_1 import find_namesakes, get_courses_data


class TestNamesakes:
    def test_find_namesakes_returns_list(self, sample_courses_data):
        """Тест, что функция возвращает список"""
        courses, mentors, durations = sample_courses_data
        result = find_namesakes(courses, mentors, durations)
        assert isinstance(result, list)

    def test_find_namesakes_structure(self, sample_courses_data):
        """Тест структуры возвращаемых данных"""
        courses, mentors, durations = sample_courses_data
        results = find_namesakes(courses, mentors, durations)

        for result in results:
            assert "course" in result
            assert "namesakes" in result
            assert isinstance(result["course"], str)
            assert isinstance(result["namesakes"], list)

    def test_find_namesakes_with_namesakes(self, courses_with_namesakes):
        """Тест поиска тёзок в курсах с тёзками"""
        courses, mentors, durations = courses_with_namesakes
        results = find_namesakes(courses, mentors, durations)

        assert len(results) == 1
        assert results[0]["course"] == "Test Course 1"
        assert "Иван Иванов" in results[0]["namesakes"]
        assert "Иван Сидоров" in results[0]["namesakes"]
        assert len(results[0]["namesakes"]) == 2

    def test_find_namesakes_without_namesakes(self, courses_without_namesakes):
        """Тест поиска тёзок в курсах без тёзок"""
        courses, mentors, durations = courses_without_namesakes
        results = find_namesakes(courses, mentors, durations)

        assert len(results) == 0

    def test_namesakes_sorted(self, courses_with_namesakes):
        """Тест, что тёзки отсортированы по алфавиту"""
        courses, mentors, durations = courses_with_namesakes
        mentors[0].extend(["Алексей Алексеев", "Алексей Петров"])  # Добавляем ещё тёзок
        results = find_namesakes(courses, mentors, durations)

        namesakes = results[0]["namesakes"]
        assert namesakes == sorted(namesakes)

    def test_real_data_consistency(self, sample_courses_data):
        """Тест согласованности реальных данных"""
        courses, mentors, durations = sample_courses_data

        # Проверяем, что количество курсов совпадает
        assert len(courses) == len(mentors) == len(durations)

        # Проверяем, что у каждого курса есть менторы
        for i, course_mentors in enumerate(mentors):
            assert len(course_mentors) > 0, f"Курс {courses[i]} не имеет менторов"


class TestSpecificCourses:
    @pytest.mark.parametrize("course_index,expected_namesakes", [
        (0,
         ["Александр Степанов", "Иван Бочаров", "Иван Маркитан", "Максим Батырев", "Максим Воронцов", "Сергей Индюков",
          "Сергей Сердюк"]),
        (1, ["Александр Бардин", "Александр Иванов", "Александр Ульянцев", "Александр Шлейко"]),
        (2, ["Александр Бардин", "Александр Иванов", "Александр Ульянцев"]),
        (3, ["Александр Беспоясов", "Александр Фитискин", "Александр Шлейко"]),
    ])
    def test_specific_course_namesakes(self, sample_courses_data, course_index, expected_namesakes):
        """Параметризованный тест для конкретных курсов"""
        courses, mentors, durations = sample_courses_data
        results = find_namesakes(courses, mentors, durations)

        course_result = next((r for r in results if r["course"] == courses[course_index]), None)
        assert course_result is not None, f"Не найден курс {courses[course_index]} в результатах"
        assert set(course_result["namesakes"]) == set(expected_namesakes)


class TestEdgeCases:
    def test_empty_data(self):
        """Тест с пустыми данными"""
        results = find_namesakes([], [], [])
        assert results == []

    def test_single_mentor(self):
        """Тест с одним ментором в курсе"""
        courses = ["Test Course"]
        mentors = [["Иван Иванов"]]
        durations = [10]

        results = find_namesakes(courses, mentors, durations)
        assert results == []

    def test_all_same_names(self):
        """Тест, когда у всех менторов одинаковые имена"""
        courses = ["Test Course"]
        mentors = [["Иван Иванов", "Иван Петров", "Иван Сидоров"]]
        durations = [10]

        results = find_namesakes(courses, mentors, durations)
        assert len(results) == 1
        assert len(results[0]["namesakes"]) == 3

    def test_mentor_with_multiple_words(self):
        """Тест с менторами, у которых несколько слов в имени"""
        courses = ["Test Course"]
        mentors = [["Иван Иванов", "Иван Петров Сидоров", "Петр Петров"]]
        durations = [10]

        results = find_namesakes(courses, mentors, durations)
        assert len(results) == 1
        assert "Иван Иванов" in results[0]["namesakes"]
        assert "Иван Петров Сидоров" in results[0]["namesakes"]


class TestIntegration:
    def test_full_integration(self, sample_courses_data):
        """Интеграционный тест полного потока"""
        courses, mentors, durations = sample_courses_data
        results = find_namesakes(courses, mentors, durations)

        # Проверяем, что найдены все курсы с тёзками
        assert len(results) == 4

        # Проверяем формат вывода
        for result in results:
            assert isinstance(result["course"], str)
            assert len(result["course"]) > 0
            assert isinstance(result["namesakes"], list)
            assert len(result["namesakes"]) > 0

            # Проверяем, что все имена в списке тёзок - строки
            for name in result["namesakes"]:
                assert isinstance(name, str)
                assert len(name) > 0