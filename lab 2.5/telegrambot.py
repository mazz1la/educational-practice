import telebot
from telebot import types

bot = telebot.TeleBot('7754282453:AAH7qEPv9Xau9n4x2UOBSDDIp21tDapAuRY')

@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, f"Здраствуйте {message.from_user.first_name} это мой первый бот, не судите строго <3")



bot.polling(none_stop = True)