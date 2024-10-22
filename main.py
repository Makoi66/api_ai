import asyncio
import config
import gemini
import aimlapi


from os import remove
from aiogram import F
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.enums import ParseMode

whitelist = config.whitelist
TOKEN = config.tele_token
bot = Bot(TOKEN)
dp = Dispatcher()

global model
global choose
model = 0




# --- Main Menu ---

menu = InlineKeyboardBuilder()
for e in config.models:
    menu.row(InlineKeyboardButton(text=e, callback_data=e))

# -----------------


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    if message.chat.id in whitelist:
        global choose
        choose = await message.answer("Choose the model", reply_markup=menu.as_markup(resize_keyboard=True))


@dp.message(F.text, Command('clear'))
async def command_start_handler(message: Message) -> None:
    if message.chat.id in whitelist:
        global model
        if model == 0:
            gemini.create(config.models[0])
        if model == 1:
            #chatgpt
            pass
        if model == 2:
            #claude
            pass
        if model == 3:
            gemini.create(config.models[3])
        await message.answer(f'{config.models[model]}: context deleted')


@dp.message()
async def command_start_handler(message: Message) -> None:
    if message.chat.id in whitelist:
        try:
            img = message.photo
            if img is None:
                img = False
                tgmess = message.text
            else:
                img = True
                await bot.download(message.photo[-1], 'img.png')
                tgmess = message.caption
            ans = ''
            if model == 0 or model == 3:
                #gemini-1.5-pro-002
                ans = gemini.request(tgmess, img)
            elif model == 1:
                #gpt-4o
                pass
                #ans = aimlapi.generate_text(config.models[1], tgmess)
            elif model == 2:
                #claude
                pass
                #ans = aimlapi.generate_text(config.models[3], tgmess)
            if img:
                remove('img.png')
            await message.answer(ans, parse_mode=ParseMode.MARKDOWN)
        except Exception as e:
            print(e)
            await message.answer('!Error: retry', parse_mode=ParseMode.MARKDOWN)


@dp.callback_query()
async def vvcallback(callback: types.CallbackQuery) -> None:
    if callback.message.chat.id in whitelist:
        global model
        global choose
        if callback.data == config.models[0]:
            gemini.create(callback.data)
            model = 0
        elif callback.data == config.models[1]:
            #chatgpt
            model = 1
            pass
        elif callback.data == config.models[2]:
            #claude
            model = 2
            pass
        elif callback.data == config.models[3]:
            gemini.create(callback.data)
            model = 3
        else:
            raise Exception
        await choose.edit_text(f'Selected model: {callback.data}')


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())