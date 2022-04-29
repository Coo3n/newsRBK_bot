from asyncio.windows_events import NULL
from email import message, message_from_file
from aiogram import Bot, types
import time 
import random
import requests
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text
from config import TOKEN, vk_token
from req import parse_site, choice_rubric, result_list
import keyboard as kb
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.exceptions import Throttled


bot = Bot(token=TOKEN)
storage = MemoryStorage()
dispetcher = Dispatcher(bot, storage = storage)
finish_str = ""

async def anti_flood(*args, **kwargs):
    ans = args[0]
    await ans.answer("Прекрати ломать бота, кликай спокойней")

@dispetcher.message_handler(commands=['start'])
@dispetcher.throttled(anti_flood, rate=1)
async def process_start_command(message: types.Message):
    await message.reply("Добро пожаловать, " + message.from_user.first_name + "!", reply_markup = kb.main_menu)

@dispetcher.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Данный Бот предоставляет услуги новостного канала! Чтобы получить новость - нажмите на одну из предложенных кнопок!")


@dispetcher.callback_query_handler(text_contains="btn")
async def process_callback_btnCats(call: types.CallbackQuery):
    group = ["kotikihujotiki", "v.kote"]
    url = f"https://api.vk.com/method/wall.get?domain={group[random.randint(0, len(group)-1)]}&count=10&access_token={vk_token}&v=5.81"
    req = requests.get(url)
    src = req.json()

    posts = src["response"]["items"]

    result = []

    for post in posts:
        try:
            if "attachments" in post:
                post = post["attachments"]
            if post[0]["type"] == "photo":
                result.append(post[0]["photo"]["sizes"][-1]["url"])
        except Exception:
            print("Oups!")

    await bot.send_photo(call.from_user.id, result[random.randint(0, len(result)-1)])


@dispetcher.message_handler(Text(equals="🆕Последняя новость"))
@dispetcher.throttled(anti_flood, rate = 1.5)
async def get_last_new(message: types.Message):
    try:
        choice_rubric(finish_str,"Последняя новость")
        cnt_str = 1
        for news in result_list:
            if cnt_str == 2:
                res = title + '\n' + news
                await message.answer(res, reply_markup = kb.inline_menu)
                cnt_str = 1
            elif cnt_str == 1:
                title = news
                cnt_str+=1
        result_list.clear()
    except:
        await message.answer("Пожалуйста, выбери еще раз рубрику!", reply_markup = kb.main_menu)

@dispetcher.message_handler(Text(equals="📰Текущие новости"))
@dispetcher.throttled(anti_flood, rate=2)
async def get_lastFive_news(message: types.Message):
    try:
        choice_rubric(finish_str, "Текущие новости")
        cnt_str = 1
        for news in result_list:
            if cnt_str == 2:
                res = "🔥 " + title + '\n' + news
                await message.answer(res, reply_markup = kb.inline_menu)
                cnt_str = 1
            elif cnt_str == 1:
                title = news
                cnt_str+=1
        result_list.clear()
    except:
        await message.answer("Пожалуйста, выбери еще раз рубрику!", reply_markup = kb.main_menu)

@dispetcher.message_handler()
async def switch_menu(message: types.Message):
    global finish_str
    match message.text:
        case "💼Политика":
            finish_str = "Политика"
            await message.answer("💼Политика", reply_markup=kb.other_menu)
        case "📉Экономика":
            finish_str = "Экономика"
            await message.answer("📉Экономика", reply_markup=kb.other_menu)
        case "🏋Спорт":
            finish_str = "Спорт"
            await message.answer("🏋Спорт", reply_markup=kb.other_menu)
        case "💰Бизнес":
            finish_str = "Бизнес"
            await message.answer("💰Бизнес", reply_markup=kb.other_menu)
        case "👨‍👩‍👧‍👦Общество":
            finish_str = "Общество"
            await message.answer("👨‍👩‍👧‍👦Общество", reply_markup=kb.other_menu)
        case "🔙Главное меню":
            await message.answer("🔙Главное меню", reply_markup=kb.main_menu)
        case _:
            await message.answer("Введена неизвестная команда!" +'\n'+ "Попробуйте написать команду: /help")
        

if __name__ == '__main__':
    executor.start_polling(dispetcher,skip_updates=True)