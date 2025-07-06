import os
import json
import openai
from telebot import types

# --- API KEY через змінні оточення ---
openai_api_key = os.environ['OPENAI_API_KEY']
openai_client = openai.OpenAI(api_key=openai_api_key)
# Якщо треба змінити базу (наприклад для Groq):
# openai_client = openai.OpenAI(api_key=openai_api_key, base_url="https://api.groq.com/openai/v1")

class AI:
    settings = {"message_history_length": 10}

    # Cache managing functions
    @staticmethod
    def get_history():
        """Returns cached history"""
        with open("chat_history.json", 'r', encoding="utf-8") as f:
            return list(json.load(f))

    @classmethod
    def clear_msg_hist(cls):
        """Clears entire cache, except mentality"""
        j = cls.get_history()
        with open("chat_history.json", 'w', encoding="utf-8") as f:
            j = [j[0]]
            json.dump(j, f)

    @classmethod
    def _delete_cache(cls):
        """Deletes excessive cache depending on settings"""
        if len(cls.get_history()) - 1 > cls.settings["message_history_length"]:
            j = cls.get_history()
            with open("chat_history.json", 'w', encoding="utf-8") as f:
                j.pop(1)
                json.dump(j, f)

    @classmethod
    def _add_new_message(cls, msg: types.Message):
        hist = cls.get_history()
        with open("chat_history.json", 'w', encoding="utf-8") as f:
            # Витягуємо тільки суть повідомлення:
            content = msg.text
            # Якщо повідомлення містить конструкцію "... сказав: ..."
            if 'сказав:' in content:
                content = content.split('сказав:', 1)[-1].strip().strip('"')
            hist.append({"role": "user", "content": content})
            json.dump(hist, f)
        cls._delete_cache()

    # Send request
    @classmethod
    def send_request(cls, msg: types.Message):
        """Returns AI answer to message"""
        cls._add_new_message(msg)

        # Для нової версії openai (1.x.x)
        response = openai_client.chat.completions.create(
            # model="deepseek-r1-distill-llama-70b",
            model="gpt-4o",  # це ще новіше, ще потужніше і ще дешевше, якщо у тебе доступ є!
            messages=cls.get_history(),
            # temperature=0.7,
        )

        return response.choices[0].message.content
