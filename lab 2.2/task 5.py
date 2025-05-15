class Class:
    def __init__(self, name="NoName", value=0):
        self.name = name
        self.value = value
        print(f"Объект {self.name} с значением {self.value} создан")

    def __del__(self):
        print(f"Объект {self.name} удален")

while True:
    answer = input("Создать объект? (Да/Нет): ").lower()
    if answer == 'да':
        name = input("Введите имя объекта: ")
        value_input = input("Введите значение объекта (число): ")
        if value_input.isdigit() or (value_input.startswith('-') and value_input[1:].isdigit()):
            value = int(value_input)
        else:
            value = 0
            print("Введено неверное значение, установлено значение по умолчанию (0)")
        obj = Class(name, value)
        break
    elif answer == 'нет':
        obj = Class()
        break
    else:
        print("Error")

print(f"Имя объекта: {obj.name}")
print(f"Значение объекта: {obj.value}")


print(f"Имя объекта: {obj.name}")
print(f"Значение объекта: {obj.value}")

