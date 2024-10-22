import asyncio
import config
import gemini


from os import remove
from aiogram import F
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.enums import ParseMode

path = '//bin//api_ai//'

with open(f'{path}admin.txt', 'r') as f:
    admin = f.readlines()

global whitelist
with open(f'{path}whitelist.txt', 'r') as f:
    whitelist = []
    for e in f:
        whitelist.append(e.strip())
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
    print(message.chat.id)
    if f'{message.chat.id}' in whitelist:
        global choose
        choose = await message.answer("Choose the model", reply_markup=menu.as_markup(resize_keyboard=True))


@dp.message(F.text, Command('clear'))
async def command_start_handler(message: Message) -> None:
    if f'{message.chat.id}' in whitelist:
        global model
        if model == config.models[0] or model == config.models[1]:
            gemini.clear(f'{message.chat.id}')
        await message.answer(f'{model}: context deleted')


@dp.message(F.text, Command('add'))
async def command_start_handler(message: Message) -> None:
    if f'{message.chat.id}' in admin:
        try:
            with open(f'{path}whitelist.txt', 'a+') as f:
                f.write(f'\n{message.text.split()[-1]}')
            whitelist.append(message.text.split()[-1])
            await message.answer('OK', parse_mode=ParseMode.MARKDOWN)
        except:
            await message.answer('!Error', parse_mode=ParseMode.MARKDOWN)


@dp.message(F.text, Command('del'))
async def command_start_handler(message: Message) -> None:
    if f'{message.chat.id}' in admin:
        try:
            whitelist.remove(message.text.split()[-1])
            with open(f'{path}whitelist.txt', 'w') as f:
                for i in range(len(whitelist)):
                    if i == len(whitelist)-1:
                        f.write(f'{whitelist[i]}')
                    else:
                        f.write(f'{whitelist[i]}\n')
            await message.answer('OK', parse_mode=ParseMode.MARKDOWN)
        except:
            await message.answer('!Error', parse_mode=ParseMode.MARKDOWN)


@dp.message(F.text, Command('get'))
async def command_start_handler(message: Message) -> None:
    if f'{message.chat.id}' in admin:
        try:
            lst = ''
            for i in range(len(whitelist)):
                if i == len(whitelist) - 1:
                    lst += f'{whitelist[i]}'
                else:
                    lst += f'{whitelist[i]}\n'
            await message.answer(lst, parse_mode=ParseMode.MARKDOWN)
        except:
            await message.answer('!Error', parse_mode=ParseMode.MARKDOWN)


@dp.message()
async def command_start_handler(message: Message) -> None:
    if f'{message.chat.id}' in whitelist:
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
            if model == config.models[0] or model == config.models[1]:
                #gemini
                ans = gemini.request(model, tgmess, img, f'{message.chat.id}')
            if img:
                remove('img.png')
            await message.answer(ans, parse_mode=ParseMode.MARKDOWN)
        except Exception as e:
            print(e)
            await message.answer('!Error: retry', parse_mode=ParseMode.MARKDOWN)


@dp.callback_query()
async def vvcallback(callback: types.CallbackQuery) -> None:
    if f'{callback.message.chat.id}' in whitelist:
        global model
        global choose
        if callback.data == config.models[0]:
            model = config.models[0]
            gemini.clear(f'{callback.message.chat.id}')
        elif callback.data == config.models[1]:
            model = config.models[1]
            gemini.clear(f'{callback.message.chat.id}')
        else:
            raise Exception
        await choose.edit_text(f'Selected model: {callback.data}')


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
