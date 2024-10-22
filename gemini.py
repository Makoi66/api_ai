import google.generativeai as genai
import PIL.Image

import config

genai.configure(api_key=config.models_tokens['gemini'])

global chat


def create(ver) -> None:
    global chat
    model = genai.GenerativeModel(ver)
    chat = model.start_chat(history=[])


def request(mess, photo):
    global chat
    if photo:
        img = PIL.Image.open('img.png')
        response = chat.send_message(content=[mess, img], safety_settings=config.gemini_settings)
    else:
        response = chat.send_message(content=mess, safety_settings=config.gemini_settings)
    # print(chat.history)
    return response.text


if __name__ == '__main__':
    model = genai.list_models()
    for e in model:
        if 'generateContent' in e.supported_generation_methods:
            print(e.name)