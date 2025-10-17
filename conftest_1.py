import pytest
from main_1 import get_courses_data

@pytest.fixture
def sample_courses_data():
    """Фикстура с исходными данными курсов"""
    return get_courses_data()

@pytest.fixture
def courses_with_namesakes():
    """Фикстура с курсами, где есть тёзки"""
    courses = ["Test Course 1", "Test Course 2"]
    mentors = [
        ["Иван Иванов", "Петр Петров", "Иван Сидоров", "Мария Иванова"],
        ["Анна Петрова", "Сергей Сергеев"]
    ]
    durations = [10, 15]
    return courses, mentors, durations

@pytest.fixture
def courses_without_namesakes():
    """Фикстура с курсами, где нет тёзок"""
    courses = ["Test Course 3"]
    mentors = [
        ["Иван Иванов", "Петр Петров", "Мария Сидорова"]
    ]
    durations = [12]
    return courses, mentors, durations