class Numbers:
    def __init__(self):
        self.num1 = float(input("Введите первое число: "))
        self.num2 = float(input("Введите второе число: "))

    def show(self):
        print("Первое число:", self.num1)
        print("Второе число:", self.num2)
        print("Сумма чисел:", self.num1 + self.num2)
        print("Наибольшее число:", max(self.num1, self.num2))

    def update(self, num1, num2):
        self.num1 = num1
        self.num2 = num2

    def change_number(self):
        while True:
            choice = input("Что хотите изменить? 1 - первое число, 2 - второе число, 0 - выход: ")
            if choice == '1':
                self.num1 = float(input("Введите новое первое число: "))
            elif choice == '2':
                self.num2 = float(input("Введите новое второе число: "))
            elif choice == '0':
                break
            else:
                print("Неверный выбор, попробуйте снова.")


numbers = Numbers()

print("Введённые числа:")
numbers.show()

numbers.change_number()
print("После изменений:")
numbers.show()
