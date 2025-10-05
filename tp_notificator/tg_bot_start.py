import telebot
from config import TG_TOKEN


bot = telebot.TeleBot(TG_TOKEN)

@bot.message_handler(commands=['start'])
def send_tg_msg(message):
    bot.send_message(message.chat.id, f'Привет, твой ID: {message.chat.id}.\nДля получения рассылки отправь ID администратору.')

if __name__ == '__main__':
    bot.infinity_polling()

