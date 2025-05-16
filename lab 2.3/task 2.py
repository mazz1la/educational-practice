class Worker:
    def __init__(self, name, surname, rate, days):
        self.__name = name
        self.__surname = surname
        self.__rate = rate
        self.__days = days

    def get_name(self):
        return self.__name

    def get_surname(self):
        return self.__surname

    def get_rate(self):
        return self.__rate

    def get_days(self):
        return self.__days

    def get_salary(self):
        salary = self.__rate * self.__days
        print(f"Зарплата работника {self.__name} {self.__surname}: {salary}")
        return salary

worker = Worker("Алиев", "Эмиль", 30000, 30)
worker.get_salary()

print("Имя:", worker.get_name())
print("Фамилия:", worker.get_surname())
print("Ставка:", worker.get_rate())
print("Дней отработано:", worker.get_days())