class Student:
    def __init__(self, surname, date_of_birth, number_group, progress):
        self.surname = surname
        self.date_of_birth = date_of_birth
        self.number_group = number_group
        self.progress = progress

    def update_surname(self, new_surname):
        self.surname = new_surname

    def update_date_of_birth(self, new_date_of_birth):
        self.date_of_birth = new_date_of_birth

    def update_number_group(self, new_number_group):
        self.number_group = new_number_group

    def info(self):
        return (f"Фамилия: {self.surname}, Дата рождения: {self.date_of_birth}, "
                f"Номер группы: {self.number_group}, Успеваемость: {self.progress}")

def info_all_students(students):
    for student in students:
        print(student.info())

students = [
    Student("Раковицэ", "05.02.2007", "634", [5, 5, 5, 5, 5]),
    Student("Саркисян", "13.01.2007", "634", [5, 4, 5, 5, 5]),
    Student("Алиев", "17.05.2007", "634", [5, 5, 3, 5, 4])
]

while True:
        choice = int(input("1 - Вывести всех студентов\n2 - Изменить данные у студента\n3 - Завершить\n"))
        if choice == 1:
            info_all_students(students)
        elif choice == 2:
            info_all_students(students)
            student_index = int(input("\nВведите номер студента для изменения (или 0 для выхода): ")) - 1
            if student_index == -1:
                break

            student = students[student_index]
            print(f"\nВыбран студент: {student.info()}")

            print("\nЧто вы хотите изменить?\n1. Фамилию\n2. Дату рождения\n3. Номер группы")

            choice_2 = input("Введите номер действия: ")

            if choice_2 == "1":
                new_surname = input("Введите новую фамилию: ")
                student.update_surname(new_surname)
            elif choice_2 == "2":
                new_date_of_birth = input("Введите новую дату рождения: ")
                student.update_date_of_birth(new_date_of_birth)
            elif choice_2 == "3":
                new_number_group = input("Введите новый номер группы: ")
                student.update_number_group(new_number_group)
            else:
                print("Неверный выбор.")
        elif choice == 3:
            break