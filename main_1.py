courses = ["Java-разработчик с нуля", "Fullstack-разработчик на Python", "Python-разработчик с нуля",
           "Frontend-разработчик с нуля"]
mentors = [
    ["Филипп Воронов", "Анна Юшина", "Иван Бочаров", "Анатолий Корсаков", "Юрий Пеньков", "Илья Сухачев",
     "Иван Маркитан", "Ринат Бибиков", "Вадим Ерошевичев", "Тимур Сейсембаев", "Максим Батырев", "Никита Шумский",
     "Алексей Степанов", "Денис Коротков", "Антон Глушков", "Сергей Индюков", "Максим Воронцов", "Евгений Грязнов",
     "Константин Виролайнен", "Сергей Сердюк", "Павел Дерендяев"],
    ["Евгений Шмаргунов", "Олег Булыгин", "Александр Бардин", "Александр Иванов", "Кирилл Табельский",
     "Александр Ульянцев", "Роман Гордиенко", "Адилет Асканжоев", "Александр Шлейко", "Алена Батицкая", "Денис Ежков",
     "Владимир Чебукин", "Эдгар Нуруллин", "Евгений Шек", "Максим Филипенко", "Елена Никитина"],
    ["Евгений Шмаргунов", "Олег Булыгин", "Дмитрий Демидов", "Кирилл Табельский", "Александр Ульянцев",
     "Александр Бардин", "Александр Иванов", "Антон Солонилин", "Максим Филипенко", "Елена Никитина", "Азамат Искаков",
     "Роман Гордиенко"],
    ["Владимир Чебукин", "Эдгар Нуруллин", "Евгений Шек", "Валерий Хаслер", "Татьяна Тен", "Александр Фитискин",
     "Александр Шлейко", "Алена Батицкая", "Александр Беспоясов", "Денис Ежков", "Николай Лопин", "Михаил Ларченко"]
]
durations = [14, 20, 12, 20]


def find_namesakes(courses, mentors, durations):
    """Основная функция для поиска тёзок"""
    courses_list = []
    for course, mentor, duration in zip(courses, mentors, durations):
        course_dict = {"title": course, "mentors": mentor, "duration": duration}
        courses_list.append(course_dict)

    results = []
    for course in courses_list:
        names = [m.split()[0] for m in course["mentors"]]
        unique_names = set(names)

        same_name_list = []
        for name in unique_names:
            if names.count(name) > 1:
                for mentor in course["mentors"]:
                    if mentor.split()[0] == name:
                        same_name_list.append(mentor)

        same_name_list = sorted(same_name_list)
        if same_name_list:
            results.append({
                "course": course["title"],
                "namesakes": same_name_list
            })

    return results


def get_courses_data():
    """Возвращает исходные данные"""
    return courses, mentors, durations


if __name__ == "__main__":
    results = find_namesakes(courses, mentors, durations)
    for result in results:
        print(f'На курсе {result["course"]} есть тёзки: {", ".join(result["namesakes"])}')