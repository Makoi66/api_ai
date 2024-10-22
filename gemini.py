import google.generativeai as genai
import PIL.Image

import config

genai.configure(api_key=config.models_tokens['gemini'])

global chat

global history
history = {}

with open('whitelist.txt', 'r') as f:
    for e in f:
        history[e.strip()] = []

def clear(person):
    history[person] = []

def request(ver, mess, photo, person):
    model = genai.GenerativeModel(ver)
    chat = model.start_chat(history=history[person])
    if photo:
        img = PIL.Image.open('img.png')
        response = chat.send_message(content=[mess, img], safety_settings=config.gemini_settings)
    else:
        response = chat.send_message(content=mess, safety_settings=config.gemini_settings)
    history[person] = chat.history
    print(chat.history)
    return response.text


if __name__ == '__main__':
    model = genai.list_models()
    for e in model:
        if 'generateContent' in e.supported_generation_methods:
            print(e.name)