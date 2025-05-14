from datetime import datetime

class Train:
    def init(self, destination, number, time):
        self.destination = destination
        self.number = number
        self.time = datetime.strptime(time, "%H:%M")

    def info(self):
        return (f"Пункт назначения: {self.destination}, Номер поезда: {self.number}, "
                f"Время отправления: {self.time.strftime('%H:%M')}")

trains = []

while True:
    print("1. Добавить поезд\n2. Найти поезд\n3. Выход")
    choice = input("Выберите: ")

    if choice == "1":
        destination = input("Пункт назначения: ")
        number_train = input("Номер поезда: ")
        time = input("Время отправления (формат ЧЧ:ММ): ")
        trains.append(Train(destination, number_train, time))

    elif choice == "2":
        i = input("Введите номер поезда: ")
        for train in trains:
            if train.number == i:
                print(train.info())
                break
        else:
            print("Не найден.")

    elif choice == "3":
        break