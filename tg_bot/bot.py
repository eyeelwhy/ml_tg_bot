import os
import telebot
import logging
from config import BOT_TOKEN
from handlers import register_handlers

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

bot = telebot.TeleBot(BOT_TOKEN)
user_states = {}

register_handlers(bot, user_states)

if __name__ == '__main__':
    print("Бот запущен!")
    bot.infinity_polling()