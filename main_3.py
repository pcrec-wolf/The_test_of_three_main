courses = ["Java-разработчик с нуля", "Fullstack-разработчик на Python", "Python-разработчик с нуля", "Frontend-разработчик с нуля"]
mentors = [
    ["Филипп Воронов", "Анна Юшина", "Иван Бочаров", "Анатолий Корсаков", "Юрий Пеньков", "Илья Сухачев", "Иван Маркитан", "Ринат Бибиков", "Вадим Ерошевичев", "Тимур Сейсембаев", "Максим Батырев", "Никита Шумский", "Алексей Степанов", "Денис Коротков", "Антон Глушков", "Сергей Индюков", "Максим Воронцов", "Евгений Грязнов", "Константин Виролайнен", "Сергей Сердюк", "Павел Дерендяев"],
    ["Евгений Шмаргунов", "Олег Булыгин", "Александр Бардин", "Александр Иванов", "Кирилл Табельский", "Александр Ульянцев", "Роман Гордиенко", "Адилет Асканжоев", "Александр Шлейко", "Алена Батицкая", "Денис Ежков", "Владимир Чебукин", "Эдгар Нуруллин", "Евгений Шек", "Максим Филипенко", "Елена Никитина"],
    ["Евгений Шмаргунов", "Олег Булыгин", "Дмитрий Демидов", "Кирилл Табельский", "Александр Ульянцев", "Александр Бардин", "Александр Иванов", "Антон Солонилин", "Максим Филипенко", "Елена Никитина", "Азамат Искаков", "Роман Гордиенко"],
    ["Владимир Чебукин", "Эдгар Нуруллин", "Евгений Шек", "Валерий Хаслер", "Татьяна Тен", "Александр Фитискин", "Александр Шлейко", "Алена Батицкая", "Александр Беспоясов", "Денис Ежков", "Николай Лопин", "Михаил Ларченко"]
]
durations = [14, 20, 12, 20]

def analyze_courses_relationship(courses, mentors, durations):
    """Анализирует связь между продолжительностью курсов и количеством преподавателей"""
    courses_list = []
    for course, mentor, duration in zip(courses, mentors, durations):
        course_dict = {"title": course, "mentors": mentor, "duration": duration}
        courses_list.append(course_dict)

    duration_index = []
    mcount_index = []
    for index, course in enumerate(courses_list):
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

    return {
        "has_relationship": indexes_d == indexes_m,
        "duration_order": indexes_d,
        "mentors_order": indexes_m,
        "courses_list": courses_list
    }

if __name__ == "__main__":
    result = analyze_courses_relationship(courses, mentors, durations)
    print("Связь есть" if result["has_relationship"] else "Связи нет")
    print(f"Порядок курсов по длительности: {result['duration_order']}")
    print(f"Порядок курсов по количеству преподавателей: {result['mentors_order']}")