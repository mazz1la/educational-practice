class Calculation:
    def init(self):
        self.line = ""

    def set(self, text):
        self.line = text

    def add(self, symbol):
        self.line += symbol

    def get(self):
        return self.line

    def last(self):
        if len(self.line) == 0:
            return ""
        else:
            return self.line[-1]

    def delete_last(self):
        self.line = self.line[:-1]



calc = Calculation()

calc.set("555")
print("Текущая строка:", calc.get())

calc.add("6")
print("После добавления символа:", calc.get())

last_char = calc.last()
print("Последний символ:", last_char)

calc.delete_last()
print("После удаления последнего символа:", calc.get())
