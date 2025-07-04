import json
import openai


file = open("API_key.json", 'r')
API_KEY = json.load(file)["key_openai"]
file.close()

openai.api_key = API_KEY

responce = openai.ChatCompletion(
    model="chat-gpt-3.5-turbo",
    message=[
        {"role": "user"},
        {"content": "Hi, how are you?"}
    ]
)
