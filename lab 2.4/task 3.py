import sqlite3
import psutil
from datetime import datetime

conn = sqlite3.connect("monitor.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS system_monitor (
    id INTEGER PRIMARY KEY,
    time TEXT,
    cpu REAL,
    ram INTEGER,
    disk REAL
)
""")
conn.commit()

def save_data():
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().used // (1024 * 1024)
    disk = psutil.disk_usage('/').percent
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("INSERT INTO system_monitor (time, cpu, ram, disk) VALUES (?, ?, ?, ?)",
                   (now, cpu, ram, disk))
    conn.commit()
    print("Данные сохранены!")

def show_data():
    cursor.execute("SELECT * FROM system_monitor")
    data = cursor.fetchall()
    if not data:
        print("Нет сохранённых данных.\n")
        return
    for row in data:
        print(f"ID: {row[0]} | Время: {row[1]} | CPU: {row[2]}% | RAM: {row[3]} МБ | Диск: {row[4]}%")
    print()

while True:
    print("1 - Сохранить данные")
    print("2 - Показать данные")
    print("3 - Выход")
    choice = input("Выберите: ")
    if choice == "1":
        save_data()
    elif choice == "2":
        show_data()
    elif choice == "3":
        break
    else:
        print("Некорректный ввод")