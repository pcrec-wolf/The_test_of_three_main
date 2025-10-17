courses = [
    "Java-разработчик с нуля",
    "Fullstack-разработчик на Python",
    "Python-разработчик с нуля",
    "Frontend-разработчик с нуля"
]
mentors = [
    ["Филипп Воронов", "Анна Юшина", "Иван Бочаров", "Анатолий Корсаков", "Юрий Пеньков", "Илья Сухачев", "Иван Маркитан", "Ринат Бибиков", "Вадим Ерошевичев", "Тимур Сейсембаев", "Максим Батырев", "Никита Шумский", "Алексей Степанов", "Денис Коротков", "Антон Глушков", "Сергей Индюков", "Максим Воронцов", "Евгений Грязнов", "Константин Виролайнен", "Сергей Сердюк", "Павел Дерендяев"],
    ["Евгений Шмаргунов", "Олег Булыгин", "Александр Бардин", "Александр Иванов", "Кирилл Табельский", "Александр Ульянцев", "Роман Гордиенко", "Адилет Асканжоев", "Александр Шлейко", "Алена Батицкая", "Денис Ежков", "Владимир Чебукин", "Эдгар Нуруллин", "Евгений Шек", "Максим Филипенко", "Елена Никитина"],
    ["Евгений Шмаргунов", "Олег Булыгин", "Дмитрий Демидов", "Кирилл Табельский", "Александр Ульянцев", "Александр Бардин", "Александр Иванов", "Антон Солонилин", "Максим Филипенко", "Елена Никитина", "Азамат Искаков", "Роман Гордиенко"],
    ["Владимир Чебукин", "Эдгар Нуруллин", "Евгений Шек", "Валерий Хаслер", "Татьяна Тен", "Александр Фитискин", "Александр Шлейко", "Алена Батицкая", "Александр Беспоясов", "Денис Ежков", "Николай Лопин", "Михаил Ларченко"]
]
durations = [14, 20, 12, 20]

def find_extreme_courses(courses, mentors, durations):
    """Основная функция для поиска самых коротких и длинных курсов"""
    courses_list = []
    for course, mentor_list, duration in zip(courses, mentors, durations):
        course_dict = {
            "title": course,
            "mentors": mentor_list,
            "duration": duration
        }
        courses_list.append(course_dict)

    min_duration = min(durations)
    max_duration = max(durations)

    maxes = []
    minis = []
    for index, duration in enumerate(durations):
        if duration == max_duration:
            maxes.append(index)
        elif duration == min_duration:
            minis.append(index)

    courses_min = []
    courses_max = []
    for id in minis:
        courses_min.append(courses_list[id]["title"])
    for id in maxes:
        courses_max.append(courses_list[id]["title"])

    return {
        "shortest": {
            "courses": courses_min,
            "duration": min_duration
        },
        "longest": {
            "courses": courses_max,
            "duration": max_duration
        }
    }

def get_courses_data():
    """Возвращает исходные данные"""
    return courses, mentors, durations

if __name__ == "__main__":
    result = find_extreme_courses(courses, mentors, durations)
    print(f'Самый короткий курс(ы): {", ".join(result["shortest"]["courses"])} - {result["shortest"]["duration"]} месяца(ев)')
    print(f'Самый длинный курс(ы): {", ".join(result["longest"]["courses"])} - {result["longest"]["duration"]} месяца(ев)')