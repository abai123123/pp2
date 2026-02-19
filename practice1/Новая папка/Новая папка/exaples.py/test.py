# Создаем список словарей
students = [
    {"name": "Абай", "surname": "Рустембаев", "gpa": 3.8},
    {"name": "Иван", "surname": "Иванов", "gpa": 3.2},
    {"name": "Алина", "surname": "Серикова", "gpa": 4.0}
]

# Выводим GPA каждого студента
print("Список GPA студентов:")
for student in students:
    print(f"Студент: {student['name']}, GPA: {student['gpa']}")