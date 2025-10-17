import pytest
from main_3 import analyze_courses_relationship


class TestCoursesRelationship:
    def test_analyze_returns_dict(self, sample_courses_data):
        """Тест, что функция возвращает словарь"""
        courses, mentors, durations = sample_courses_data
        result = analyze_courses_relationship(courses, mentors, durations)
        assert isinstance(result, dict)

    def test_result_structure(self, sample_courses_data):
        """Тест структуры возвращаемых данных"""
        courses, mentors, durations = sample_courses_data
        result = analyze_courses_relationship(courses, mentors, durations)

        assert "has_relationship" in result
        assert "duration_order" in result
        assert "mentors_order" in result
        assert "courses_list" in result
        assert isinstance(result["has_relationship"], bool)
        assert isinstance(result["duration_order"], list)
        assert isinstance(result["mentors_order"], list)
        assert isinstance(result["courses_list"], list)

    def test_relationship_detection_positive(self, courses_with_relationship):
        """Тест обнаружения связи, когда она есть"""
        courses, mentors, durations = courses_with_relationship
        result = analyze_courses_relationship(courses, mentors, durations)

        assert result["has_relationship"] == True
        assert result["duration_order"] == result["mentors_order"]

    def test_relationship_detection_negative(self, courses_without_relationship):
        """Тест обнаружения отсутствия связи, когда её нет"""
        courses, mentors, durations = courses_without_relationship
        result = analyze_courses_relationship(courses, mentors, durations)

        assert result["has_relationship"] == False
        assert result["duration_order"] != result["mentors_order"]

    def test_real_data_no_relationship(self, sample_courses_data):
        """Тест реальных данных (должны показывать отсутствие связи)"""
        courses, mentors, durations = sample_courses_data
        result = analyze_courses_relationship(courses, mentors, durations)

        # Проверяем, что в реальных данных связи нет
        assert result["has_relationship"] == False

        # Проверяем конкретные ожидаемые порядки из задания
        expected_duration_order = [2, 0, 1, 3]  # Python, Java, Fullstack, Frontend
        expected_mentors_order = [2, 3, 1, 0]  # Python, Frontend, Fullstack, Java

        assert result["duration_order"] == expected_duration_order
        assert result["mentors_order"] == expected_mentors_order


class TestSortingLogic:
    def test_duration_index_sorting(self, sample_courses_data):
        """Тест корректности сортировки по длительности"""
        courses, mentors, durations = sample_courses_data
        result = analyze_courses_relationship(courses, mentors, durations)

        # Проверяем, что индексы отсортированы по возрастанию длительности
        courses_list = result["courses_list"]
        duration_order = result["duration_order"]

        durations_sorted = [courses_list[idx]["duration"] for idx in duration_order]
        assert durations_sorted == sorted(durations_sorted)

    def test_mentors_index_sorting(self, sample_courses_data):
        """Тест корректности сортировки по количеству преподавателей"""
        courses, mentors, durations = sample_courses_data
        result = analyze_courses_relationship(courses, mentors, durations)

        # Проверяем, что индексы отсортированы по возрастанию количества преподавателей
        courses_list = result["courses_list"]
        mentors_order = result["mentors_order"]

        mentors_count_sorted = [len(courses_list[idx]["mentors"]) for idx in mentors_order]
        assert mentors_count_sorted == sorted(mentors_count_sorted)

    def test_same_duration_ordering(self, courses_same_duration_different_mentors):
        """Тест порядка при одинаковой длительности курсов"""
        courses, mentors, durations = courses_same_duration_different_mentors
        result = analyze_courses_relationship(courses, mentors, durations)

        # При одинаковой длительности порядок должен сохранять исходную последовательность
        # (так как sort() в Python стабилен)
        assert result["duration_order"] == [0, 1, 2]

    def test_same_mentors_ordering(self, courses_same_mentors_different_duration):
        """Тест порядка при одинаковом количестве преподавателей"""
        courses, mentors, durations = courses_same_mentors_different_duration
        result = analyze_courses_relationship(courses, mentors, durations)

        # При одинаковом количестве преподавателей порядок должен сохранять исходную последовательность
        assert result["mentors_order"] == [0, 1, 2]


class TestEdgeCases:
    def test_single_course(self):
        """Тест с одним курсом"""
        courses = ["Single Course"]
        mentors = [["Mentor 1"]]
        durations = [10]

        result = analyze_courses_relationship(courses, mentors, durations)

        assert result["has_relationship"] == True
        assert result["duration_order"] == [0]
        assert result["mentors_order"] == [0]

    def test_empty_data(self):
        """Тест с пустыми данными"""
        result = analyze_courses_relationship([], [], [])

        assert result["has_relationship"] == True
        assert result["duration_order"] == []
        assert result["mentors_order"] == []
        assert result["courses_list"] == []

    def test_two_identical_courses(self):
        """Тест с двумя идентичными курсами"""
        courses = ["Course 1", "Course 2"]
        mentors = [["Mentor A", "Mentor B"], ["Mentor C", "Mentor D"]]
        durations = [10, 10]

        result = analyze_courses_relationship(courses, mentors, durations)

        assert result["has_relationship"] == True
        assert result["duration_order"] == [0, 1]
        assert result["mentors_order"] == [0, 1]


class TestIntegration:
    def test_consistency_with_original_data(self, sample_courses_data):
        """Интеграционный тест согласованности с исходными данными"""
        courses, mentors, durations = sample_courses_data
        result = analyze_courses_relationship(courses, mentors, durations)

        # Проверяем, что courses_list корректно создан
        assert len(result["courses_list"]) == len(courses)

        for i, course_dict in enumerate(result["courses_list"]):
            assert course_dict["title"] == courses[i]
            assert course_dict["mentors"] == mentors[i]
            assert course_dict["duration"] == durations[i]

    def test_index_correctness(self, sample_courses_data):
        """Тест корректности индексов в результатах"""
        courses, mentors, durations = sample_courses_data
        result = analyze_courses_relationship(courses, mentors, durations)

        # Проверяем, что все индексы в допустимом диапазоне
        max_index = len(courses) - 1

        for idx in result["duration_order"]:
            assert 0 <= idx <= max_index

        for idx in result["mentors_order"]:
            assert 0 <= idx <= max_index

        # Проверяем, что все индексы уникальны и покрывают весь диапазон
        assert sorted(result["duration_order"]) == list(range(len(courses)))
        assert sorted(result["mentors_order"]) == list(range(len(courses)))