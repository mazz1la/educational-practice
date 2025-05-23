import telebot
import threading
import random
import requests
import os
from datetime import datetime, timedelta
import time as time_module
from telebot import types
from yandex_music import Client
from config import TOKEN, OPENWEATHER_API_KEY, CAT_API_KEY, YANDEX_MUSIC_TOKEN

bot = telebot.TeleBot(TOKEN)

# Временное хранилище данных в памяти
user_data = {}
reminders = []
expenses = []
todos = []


# --- Общие функции ---
def create_main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = ["🎵 Музыка", "🌤 Погода", "⏰ Таймер", "🔔 Напоминание",
               "💰 Расходы", "📊 Статистика", "📌 Мои дела", "😺 Котики", "📋 Помощь"]
    markup.add(*buttons)
    return markup


# --- Музыка ---
def search_yandex_music(query, count=5):
    try:
        client = Client(YANDEX_MUSIC_TOKEN).init()
        search_result = client.search(query, type_='track')
        return [{
            'artist': ', '.join(a.name for a in track.artists),
            'title': track.title,
            'duration': track.duration_ms // 1000,
            'url': max([info for info in track.get_download_info(get_direct_links=True)
                        if info.codec == 'mp3'], key=lambda x: x.bitrate_in_kbps).direct_link,
            'track_id': track.id
        } for track in search_result.tracks.results[:count]] if search_result.tracks else []
    except Exception as e:
        print(f"Yandex Music error: {e}")
        return []


@bot.message_handler(func=lambda message: message.text == "🎵 Музыка")
def handle_music(message):
    msg = bot.reply_to(message, "🎵 Введите название трека:", reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, process_music_query)


def process_music_query(message):
    query = message.text.strip()
    if not query: return bot.reply_to(message, "❌ Пустой запрос", reply_markup=create_main_keyboard())

    search_msg = bot.reply_to(message, "🔍 Ищу музыку...")
    results = search_yandex_music(query, 5)

    if not results:
        return bot.edit_message_text("❌ Ничего не найдено", chat_id=message.chat.id, message_id=search_msg.message_id)

    if len(results) == 1:
        bot.edit_message_text("⏳ Загружаю...", chat_id=message.chat.id, message_id=search_msg.message_id)
        return download_and_send_track(message.chat.id, results[0])

    markup = types.InlineKeyboardMarkup()
    for i, track in enumerate(results[:5]):
        markup.add(types.InlineKeyboardButton(
            f"{i + 1}. {track['artist']} - {track['title'][:20]}...",
            callback_data=f"ymusic_{i}"))

    user_data[message.from_user.id] = results
    bot.edit_message_text("🎵 Выберите трек:", chat_id=message.chat.id,
                          message_id=search_msg.message_id, reply_markup=markup)


def download_and_send_track(chat_id, track):
    try:
        filename = f"{random.randint(10000, 99999)}.mp3"
        with open(filename, 'wb') as f:
            f.write(requests.get(track['url']).content)

        with open(filename, 'rb') as audio:
            bot.send_audio(chat_id, audio, title=track['title'][:64],
                           performer=track['artist'][:64], duration=track['duration'])
    except Exception as e:
        bot.send_message(chat_id, f"❌ Ошибка: {str(e)}")
    finally:
        if os.path.exists(filename): os.remove(filename)


@bot.callback_query_handler(func=lambda call: call.data.startswith('ymusic_'))
def handle_music_selection(call):
    try:
        track_index = int(call.data.split('_')[1])
        track = user_data[call.from_user.id][track_index]

        bot.edit_message_text("⏳ Загружаю...", chat_id=call.message.chat.id,
                              message_id=call.message.message_id)
        download_and_send_track(call.message.chat.id, track)
    except:
        bot.answer_callback_query(call.id, "❌ Ошибка загрузки")


# --- Погода ---
@bot.message_handler(func=lambda message: message.text == "🌤 Погода")
def weather_command(message):
    msg = bot.reply_to(message, "🌤 Введите город:", reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, get_weather)


def get_weather(message):
    try:
        data = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text.strip()}"
            f"&appid={OPENWEATHER_API_KEY}&units=metric&lang=ru"
        ).json()

        if data.get("cod") != 200: raise Exception(data.get("message", "Ошибка API"))

        weather = data['weather'][0]
        bot.reply_to(message,
                     f"🌡 Погода в {data['name']}:\n"
                     f"• Температура: {data['main']['temp']:.1f}°C\n"
                     f"• Ощущается как: {data['main']['feels_like']:.1f}°C\n"
                     f"• Состояние: {weather['description'].capitalize()}\n"
                     f"• Влажность: {data['main']['humidity']}%\n"
                     f"• Ветер: {data['wind']['speed']} м/с",
                     reply_markup=create_main_keyboard())
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {str(e)}", reply_markup=create_main_keyboard())


# --- Таймер ---
@bot.message_handler(func=lambda message: message.text == "⏰ Таймер")
def timer(message):
    msg = bot.reply_to(message, "⏳ Введите секунды:", reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, process_timer)


def process_timer(message):
    try:
        seconds = int(message.text)
        if seconds <= 0: raise ValueError()
        bot.reply_to(message, f"⏳ Таймер на {seconds} сек...", reply_markup=create_main_keyboard())
        threading.Timer(seconds, lambda: bot.send_message(
            message.chat.id, "⏰ Время вышло!", reply_markup=create_main_keyboard())).start()
    except:
        bot.reply_to(message, "❌ Введите число > 0", reply_markup=create_main_keyboard())


# --- Напоминания ---
def check_reminders():
    while True:
        now = datetime.now()
        for reminder in [r for r in reminders if r['time'] <= now]:
            try:
                bot.send_message(reminder['user_id'], f"🔔 Напоминание: {reminder['text']}")
                reminders.remove(reminder)
            except:
                pass
        time_module.sleep(10)


threading.Thread(target=check_reminders, daemon=True).start()


@bot.message_handler(func=lambda message: message.text == "🔔 Напоминание")
def reminder(message):
    msg = bot.reply_to(message, "Введите текст и время (текст | ДД.ММ.ГГГГ ЧЧ:ММ или ЧЧ:ММ)",
                       reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, process_reminder)


def process_reminder(message):
    try:
        text, time_str = [p.strip() for p in message.text.split('|', 1)]
        try:
            remind_at = datetime.strptime(time_str, "%d.%m.%Y %H:%M")
        except:
            time_obj = datetime.strptime(time_str, "%H:%M").time()
            remind_at = datetime.combine(datetime.now(), time_obj)
            if remind_at < datetime.now(): remind_at += timedelta(days=1)

        reminders.append({'user_id': message.chat.id, 'text': text, 'time': remind_at})
        bot.reply_to(message, f"✅ Напоминание на {remind_at.strftime('%d.%m.%Y %H:%M')}")
    except:
        bot.reply_to(message, "❌ Неверный формат", reply_markup=create_main_keyboard())


# --- Расходы ---
@bot.message_handler(func=lambda message: message.text == "💰 Расходы")
def add_expense(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    markup.add(*["🍔 Еда", "🚌 Транспорт", "🛒 Покупки", "🏠 Жилье", "💊 Здоровье", "❌ Отмена"])
    msg = bot.reply_to(message, "📊 Выберите категорию:", reply_markup=markup)
    bot.register_next_step_handler(msg, process_expense_category)


def process_expense_category(message):
    if message.text == "❌ Отмена":
        return bot.reply_to(message, "❌ Отменено", reply_markup=create_main_keyboard())

    user_data[message.from_user.id] = {'category': message.text[2:]}
    msg = bot.reply_to(message, "💵 Введите сумму:", reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, process_expense_amount)


def process_expense_amount(message):
    try:
        amount = float(message.text.replace(',', '.'))
        if amount <= 0: raise ValueError()
        user_data[message.from_user.id]['amount'] = amount
        msg = bot.reply_to(message, "📝 Описание (необязательно):")
        bot.register_next_step_handler(msg, lambda m: save_expense(m, amount))
    except:
        bot.reply_to(message, "❌ Неверная сумма", reply_markup=create_main_keyboard())


def save_expense(message, amount):
    expenses.append({
        'user_id': message.from_user.id,
        'amount': amount,
        'category': user_data[message.from_user.id]['category'],
        'description': message.text
    })
    bot.reply_to(message, f"✅ Расход добавлен: {amount:.2f}₽", reply_markup=create_main_keyboard())


@bot.message_handler(func=lambda message: message.text == "📊 Статистика")
def show_stats(message):
    user_expenses = [e for e in expenses if e['user_id'] == message.chat.id]
    if not user_expenses: return bot.reply_to(message, "📊 Нет данных")

    total = sum(e['amount'] for e in user_expenses)
    stats = "\n".join(
        f"{e['category']}: {e['amount']:.2f}₽ ({(e['amount'] / total) * 100:.1f}%)"
        for e in user_expenses
    )
    bot.reply_to(message, f"📊 Статистика:\n{stats}\n\n💵 Всего: {total:.2f}₽")


# --- Список дел ---
@bot.message_handler(func=lambda message: message.text == "📌 Мои дела")
def show_todos(message):
    user_todos = [t for t in todos if t['user_id'] == message.chat.id]

    markup = types.InlineKeyboardMarkup()
    for task in user_todos:
        status = "✅" if task['done'] else "❌"
        markup.row(
            types.InlineKeyboardButton(f"{status} {task['text']}", callback_data=f"todo_{task['id']}"),
            types.InlineKeyboardButton("🗑", callback_data=f"del_{task['id']}")
        )
    markup.add(types.InlineKeyboardButton("➕ Добавить", callback_data="add_todo"))

    bot.send_message(message.chat.id, "📌 Ваши дела:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith(('todo_', 'del_', 'add_')))
def handle_todos(call):
    if call.data == "add_todo":
        msg = bot.send_message(call.message.chat.id, "📝 Введите задачу:")
        bot.register_next_step_handler(msg, save_todo)
    else:
        task_id = int(call.data.split('_')[1])
        if call.data.startswith('todo_'):
            for task in todos:
                if task['id'] == task_id:
                    task['done'] = not task['done']
                    break
        else:
            todos[:] = [t for t in todos if t['id'] != task_id]
        show_todos(call.message)


def save_todo(message):
    todos.append({
        'id': len(todos) + 1,
        'user_id': message.chat.id,
        'text': message.text,
        'done': False
    })
    show_todos(message)


# --- Котики ---
@bot.message_handler(func=lambda message: message.text == "😺 Котики")
def send_cat(message):
    try:
        url = requests.get('https://api.thecatapi.com/v1/images/search',
                           headers={'x-api-key': CAT_API_KEY}).json()[0]['url']
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("😻 Ещё котика!", callback_data="more_cats"))
        bot.send_photo(message.chat.id, url, reply_markup=markup)
    except:
        bot.reply_to(message, "😿 Ошибка загрузки")


@bot.callback_query_handler(func=lambda call: call.data == "more_cats")
def more_cats(call):
    send_cat(call.message)


# --- Помощь ---
@bot.message_handler(func=lambda message: message.text == "📋 Помощь")
@bot.message_handler(commands=['start', 'help'])
def help(message):
    bot.reply_to(message,
                 "📘 Доступные функции:\n\n"
                 "🎵 Музыка - Поиск музыки\n"
                 "🌤 Погода - Узнать погоду\n"
                 "⏰ Таймер - Установить таймер\n"
                 "🔔 Напоминание - Создать напоминание\n"
                 "💰 Расходы - Учет финансов\n"
                 "📊 Статистика - Статистика расходов\n"
                 "📌 Мои дела - Управление задачами\n"
                 "😺 Котики - Случайные фото котиков",
                 reply_markup=create_main_keyboard())


if __name__ == '__main__':
    print("Бот запущен...")
    bot.polling(none_stop=True)