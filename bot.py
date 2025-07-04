import json
import telebot
from ai_deepseek import AI
from telebot import types
import random


file = open("TOKEN.json", "r",)
TOKEN = json.load(file)["TOKEN"]
file.close()

bot = telebot.TeleBot(TOKEN)

with open("settings.json", 'r') as f:
    AI.settings = json.load(f)

# getting bot username
me = bot.get_me()
bot_username = '@' + me.username


@bot.message_handler(commands=["start"])
def start(msg: types.Message):
    bot.send_message(msg.chat.id, "Бот працює, ось список команд:\n\
/clear_message_hist - Очистити історію повідомлень")


@bot.message_handler(commands=["clear_message_hist"])
def clear_msg_hist(msg: types.Message):
    try:
        AI.clear_msg_hist()
        bot.send_message(msg.chat.id, "Історію повідомлень видалено" if len(AI.get_history()) == 1 else "Щось пішло не так")
    except Exception as e:
        bot.send_message(msg.chat.id, "Щось пішло не так")
        print(e)


@bot.message_handler(content_types=["text"])
def txt_handler(msg: types.Message):
    if bot_username in [word for word in msg.text.split(' ')]:
        bot.send_message(msg.chat.id, f"{AI.send_request(msg)}")

    elif len([1 for word in msg.text.split(' ') if word.strip('?!@#%^&*()').lower() in ["даша", "дашуня", "дашка"]]) > 0:
        bot.send_message(msg.chat.id, f"{AI.send_request(msg)}")

    elif random.randrange(0, 100) <= 20:
        bot.send_message(msg.chat.id, f"{AI.send_request(msg)}")
