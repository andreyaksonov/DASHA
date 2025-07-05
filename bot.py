import os
import json
import telebot
from ai_deepseek import AI
from telebot import types
import random

# Отримуємо токен із змінної оточення
TOKEN = os.environ['TELEGRAM_TOKEN']

bot = telebot.TeleBot(TOKEN)

with open("settings.json", 'r') as f:
    AI.settings = json.load(f)

# getting bot username
me = bot.get_me()
bot_username = '@' + me.username

def reply_in_topic(msg, text):
    # Відповідь саме у той топік, якщо це тема
    if hasattr(msg, "message_thread_id") and msg.message_thread_id is not None:
        bot.send_message(
            msg.chat.id,
            text,
            message_thread_id=msg.message_thread_id
        )
    else:
        bot.send_message(msg.chat.id, text)

@bot.message_handler(commands=["start"])
def start(msg: types.Message):
    reply_in_topic(msg, "Бот працює, ось список команд:\n/clear_message_hist - Очистити історію повідомлень")

@bot.message_handler(commands=["clear_message_hist"])
def clear_msg_hist(msg: types.Message):
    try:
        AI.clear_msg_hist()
        reply_in_topic(msg, "Історію повідомлень видалено" if len(AI.get_history()) == 1 else "Щось пішло не так")
    except Exception as e:
        reply_in_topic(msg, "Щось пішло не так")
        print(e)

@bot.message_handler(content_types=["text"])
def txt_handler(msg: types.Message):
    should_reply = (
        bot_username in [word for word in msg.text.split(' ')] or
        len([1 for word in msg.text.split(' ') if word.strip('?!@#%^&*()').lower() in ["даша", "дашуня", "дашка"]]) > 0 or
        random.randrange(0, 100) <= 20
    )
    if should_reply:
        reply_in_topic(msg, f"{AI.send_request(msg)}")
