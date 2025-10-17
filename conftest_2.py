import pytest

@pytest.fixture
def sample_courses_data():
    """Фикстура с исходными данными курсов"""
    courses = [
        "Java-разработчик с нуля",
        "Fullstack-разработчик на Python",
        "Python-разработчик с нуля",
        "Frontend-разработчик с нуля"
    ]
    mentors = [
        ["Филипп Воронов", "Анна Юшина"],
        ["Евгений Шмаргунов", "Олег Булыгин"],
        ["Евгений Шмаргунов", "Дмитрий Демидов"],
        ["Владимир Чебукин", "Эдгар Нуруллин"]
    ]
    durations = [14, 20, 12, 20]
    return courses, mentors, durations

@pytest.fixture
def single_shortest_course():
    """Фикстура с одним самым коротким курсом"""
    courses = ["Course 1", "Course 2", "Course 3"]
    mentors = [["Mentor 1"], ["Mentor 2"], ["Mentor 3"]]
    durations = [10, 15, 10]
    return courses, mentors, durations

@pytest.fixture
def single_longest_course():
    """Фикстура с одним самым длинным курсом"""
    courses = ["Course A", "Course B", "Course C"]
    mentors = [["Mentor A"], ["Mentor B"], ["Mentor C"]]
    durations = [10, 20, 15]
    return courses, mentors, durations

@pytest.fixture
def multiple_extreme_courses():
    """Фикстура с несколькими курсами одинаковой минимальной и максимальной длительности"""
    courses = ["Course X", "Course Y", "Course Z", "Course W"]
    mentors = [["Mentor X"], ["Mentor Y"], ["Mentor Z"], ["Mentor W"]]
    durations = [10, 20, 10, 20]
    return courses, mentors, durations

@pytest.fixture
def all_same_duration():
    """Фикстура, где все курсы одинаковой длительности"""
    courses = ["Course 1", "Course 2", "Course 3"]
    mentors = [["Mentor 1"], ["Mentor 2"], ["Mentor 3"]]
    durations = [15, 15, 15]
    return courses, mentors, durations