import pytest
from main_2 import find_extreme_courses, get_courses_data


class TestExtremeCourses:
    def test_find_extreme_courses_returns_dict(self, sample_courses_data):
        """Тест, что функция возвращает словарь"""
        courses, mentors, durations = sample_courses_data
        result = find_extreme_courses(courses, mentors, durations)
        assert isinstance(result, dict)

    def test_result_structure(self, sample_courses_data):
        """Тест структуры возвращаемых данных"""
        courses, mentors, durations = sample_courses_data
        result = find_extreme_courses(courses, mentors, durations)

        assert "shortest" in result
        assert "longest" in result
        assert "courses" in result["shortest"]
        assert "duration" in result["shortest"]
        assert "courses" in result["longest"]
        assert "duration" in result["longest"]
        assert isinstance(result["shortest"]["courses"], list)
        assert isinstance(result["longest"]["courses"], list)
        assert isinstance(result["shortest"]["duration"], int)
        assert isinstance(result["longest"]["duration"], int)

    def test_single_shortest_course(self, single_shortest_course):
        """Тест с одним самым коротким курсом"""
        courses, mentors, durations = single_shortest_course
        result = find_extreme_courses(courses, mentors, durations)

        assert len(result["shortest"]["courses"]) == 2  # Course 1 и Course 3
        assert result["shortest"]["duration"] == 10
        assert "Course 1" in result["shortest"]["courses"]
        assert "Course 3" in result["shortest"]["courses"]

    def test_single_longest_course(self, single_longest_course):
        """Тест с одним самым длинным курсом"""
        courses, mentors, durations = single_longest_course
        result = find_extreme_courses(courses, mentors, durations)

        assert len(result["longest"]["courses"]) == 1
        assert result["longest"]["duration"] == 20
        assert "Course B" in result["longest"]["courses"]

    def test_multiple_extreme_courses(self, multiple_extreme_courses):
        """Тест с несколькими курсами одинаковой минимальной и максимальной длительности"""
        courses, mentors, durations = multiple_extreme_courses
        result = find_extreme_courses(courses, mentors, durations)

        assert len(result["shortest"]["courses"]) == 2
        assert len(result["longest"]["courses"]) == 2
        assert result["shortest"]["duration"] == 10
        assert result["longest"]["duration"] == 20
        assert set(result["shortest"]["courses"]) == {"Course X", "Course Z"}
        assert set(result["longest"]["courses"]) == {"Course Y", "Course W"}

    def test_all_same_duration(self, all_same_duration):
        """Тест, когда все курсы одинаковой длительности"""
        courses, mentors, durations = all_same_duration
        result = find_extreme_courses(courses, mentors, durations)

        assert result["shortest"]["duration"] == result["longest"]["duration"]
        assert result["shortest"]["duration"] == 15
        assert len(result["shortest"]["courses"]) == 3
        assert len(result["longest"]["courses"]) == 3
        assert set(result["shortest"]["courses"]) == set(courses)
        assert set(result["longest"]["courses"]) == set(courses)


class TestRealData:
    def test_real_data_consistency(self, sample_courses_data):
        """Тест согласованности реальных данных"""
        courses, mentors, durations = sample_courses_data

        # Проверяем, что количество курсов совпадает
        assert len(courses) == len(mentors) == len(durations)

        # Проверяем, что у каждого курса есть менторы
        for i, course_mentors in enumerate(mentors):
            assert len(course_mentors) > 0, f"Курс {courses[i]} не имеет менторов"

    def test_real_data_values(self):
        """Тест конкретных значений из реальных данных"""
        courses, mentors, durations = get_courses_data()
        result = find_extreme_courses(courses, mentors, durations)

        # Проверяем конкретные значения из вашего примера
        assert result["shortest"]["duration"] == 12
        assert result["longest"]["duration"] == 20
        assert "Python-разработчик с нуля" in result["shortest"]["courses"]
        assert "Fullstack-разработчик на Python" in result["longest"]["courses"]
        assert "Frontend-разработчик с нуля" in result["longest"]["courses"]


class TestEdgeCases:
    def test_empty_data(self):
        """Тест с пустыми данными"""
        result = find_extreme_courses([], [], [])
        assert result["shortest"]["duration"] == 0  # min([]) = 0 в Python
        assert result["longest"]["duration"] == 0  # max([]) = 0 в Python
        assert result["shortest"]["courses"] == []
        assert result["longest"]["courses"] == []

    def test_single_course(self):
        """Тест с одним курсом"""
        courses = ["Single Course"]
        mentors = [["Single Mentor"]]
        durations = [10]

        result = find_extreme_courses(courses, mentors, durations)

        assert result["shortest"]["duration"] == 10
        assert result["longest"]["duration"] == 10
        assert result["shortest"]["courses"] == ["Single Course"]
        assert result["longest"]["courses"] == ["Single Course"]

    def test_negative_durations(self):
        """Тест с отрицательными длительностями"""
        courses = ["Course 1", "Course 2"]
        mentors = [["Mentor 1"], ["Mentor 2"]]
        durations = [-5, -10]

        result = find_extreme_courses(courses, mentors, durations)

        assert result["shortest"]["duration"] == -10
        assert result["longest"]["duration"] == -5
        assert "Course 2" in result["shortest"]["courses"]
        assert "Course 1" in result["longest"]["courses"]


class TestIntegration:
    def test_full_integration(self, sample_courses_data):
        """Интеграционный тест полного потока"""
        courses, mentors, durations = sample_courses_data
        result = find_extreme_courses(courses, mentors, durations)

        # Проверяем, что минимальная длительность меньше или равна максимальной
        assert result["shortest"]["duration"] <= result["longest"]["duration"]

        # Проверяем, что курсы с минимальной длительностью действительно имеют эту длительность
        for course_name in result["shortest"]["courses"]:
            course_index = courses.index(course_name)
            assert durations[course_index] == result["shortest"]["duration"]

        # Проверяем, что курсы с максимальной длительностью действительно имеют эту длительность
        for course_name in result["longest"]["courses"]:
            course_index = courses.index(course_name)
            assert durations[course_index] == result["longest"]["duration"]

        # Проверяем, что нет пересечений между самыми короткими и самыми длинными курсами
        # (кроме случая, когда все курсы одинаковой длительности)
        if result["shortest"]["duration"] != result["longest"]["duration"]:
            shortest_set = set(result["shortest"]["courses"])
            longest_set = set(result["longest"]["courses"])
            assert shortest_set.isdisjoint(longest_set)