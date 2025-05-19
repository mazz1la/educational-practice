import sqlite3

conn = sqlite3.connect("drinks.db")
cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS drinks (id INTEGER PRIMARY KEY, name TEXT, abv REAL, quantity INTEGER, price REAL)")
cursor.execute("CREATE TABLE IF NOT EXISTS cocktails (id INTEGER PRIMARY KEY, name TEXT, strength REAL, price REAL)")
cursor.execute("CREATE TABLE IF NOT EXISTS cocktail_ingredients (cocktail_id INTEGER, drink_id INTEGER, volume INTEGER)")
cursor.execute("CREATE TABLE IF NOT EXISTS sales (id INTEGER PRIMARY KEY, item TEXT, name TEXT, price REAL)")
conn.commit()

def add_drink():
    name = input("Название напитка: ")
    abv = float(input("Крепость (%): "))
    quantity = int(input("Объём (мл): "))
    price = float(input("Цена за 1 мл: "))
    cursor.execute("INSERT INTO drinks (name, abv, quantity, price) VALUES (?, ?, ?, ?)", (name, abv, quantity, price))
    conn.commit()
    print("Напиток добавлен.\n")

def show_drinks():
    cursor.execute("SELECT id, name, abv, quantity FROM drinks")
    rows = cursor.fetchall()
    for row in rows:
        print(f"{row[0]}. {row[1]} - {row[2]}% - {row[3]} мл")
    print()

def refill_stock():
    show_drinks()
    drink_id = int(input("ID напитка для пополнения: "))
    amount = int(input("Сколько мл добавить: "))
    cursor.execute("UPDATE drinks SET quantity = quantity + ? WHERE id = ?", (amount, drink_id))
    conn.commit()
    print("Склад обновлён.\n")

def create_cocktail():
    name = input("Название коктейля: ")
    ingredients = []
    total_volume = 0
    total_alcohol = 0

    while True:
        show_drinks()
        drink_id = int(input("ID напитка (0 — закончить): "))
        if drink_id == 0:
            break
        volume = int(input("Сколько мл использовать: "))
        cursor.execute("SELECT abv FROM drinks WHERE id = ?", (drink_id,))
        abv = cursor.fetchone()[0]
        ingredients.append((drink_id, volume, abv))
        total_volume += volume
        total_alcohol += volume * abv / 100

    if total_volume == 0:
        print("Коктейль не может быть пустым.\n")
        return

    strength = round(total_alcohol / total_volume * 100, 2)
    price = float(input("Цена коктейля: "))

    cursor.execute("INSERT INTO cocktails (name, strength, price) VALUES (?, ?, ?)", (name, strength, price))
    cocktail_id = cursor.lastrowid

    for ing in ingredients:
        cursor.execute("INSERT INTO cocktail_ingredients (cocktail_id, drink_id, volume) VALUES (?, ?, ?)", (cocktail_id, ing[0], ing[1]))

    conn.commit()
    print("Коктейль создан.\n")

def sell_cocktail():
    cursor.execute("SELECT id, name, price FROM cocktails")
    cocktails = cursor.fetchall()
    for c in cocktails:
        print(f"{c[0]}. {c[1]} - {c[2]} руб")
    print()

    cocktail_id = int(input("ID коктейля для продажи: "))
    cursor.execute("SELECT drink_id, volume FROM cocktail_ingredients WHERE cocktail_id = ?", (cocktail_id,))
    ingredients = cursor.fetchall()

    for drink_id, volume in ingredients:
        cursor.execute("SELECT quantity FROM drinks WHERE id = ?", (drink_id,))
        available = cursor.fetchone()[0]
        if available < volume:
            print("Недостаточно ингредиентов для продажи.\n")
            return

    # Списание остатков
    for drink_id, volume in ingredients:
        cursor.execute("UPDATE drinks SET quantity = quantity - ? WHERE id = ?", (volume, drink_id))

    cursor.execute("SELECT name, price FROM cocktails WHERE id = ?", (cocktail_id,))
    name, price = cursor.fetchone()

    cursor.execute("INSERT INTO sales (item, name, price) VALUES (?, ?, ?)", ("cocktail", name, price))
    conn.commit()
    print("Коктейль продан.\n")

def main():
    while True:
        print("Меню:")
        print("1. Добавить напиток")
        print("2. Показать напитки")
        print("3. Пополнить склад")
        print("4. Создать коктейль")
        print("5. Продать коктейль")
        print("6. Выйти")

        choice = input("Выберите действие: ")
        if choice == "1":
            add_drink()
        elif choice == "2":
            show_drinks()
        elif choice == "3":
            refill_stock()
        elif choice == "4":
            create_cocktail()
        elif choice == "5":
            sell_cocktail()
        elif choice == "6":
            print("До свидания!")
            break
        else:
            print("Неверный выбор.\n")

main()