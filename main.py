from asyncio.windows_events import NULL
from aiogram import Bot, types
import time 
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text
from config import TOKEN
from req import parse_site
from req import choice_rubric
from req import result_list
import keyboard as kb
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.exceptions import Throttled

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dispetcher = Dispatcher(bot,storage = storage)
finish_str = ""

async def anti_flood(*args, **kwargs):
    ans = args[0]
    await ans.answer("Прекрати ломать бота, кликай спокойней")

@dispetcher.message_handler(commands=['start'])
@dispetcher.throttled(anti_flood,rate=3)
async def process_start_command(message: types.Message):
    await message.reply("Привет!", reply_markup = kb.main_menu)

@dispetcher.message_handler(commands=['help'])
@dispetcher.throttled(anti_flood,rate=3)
async def process_help_command(message: types.Message):
    await message.reply("Данный Бот предоставляет услуги новостного канала! Чтобы получить новость - нажмите на одну из предложенных кнопок!")


@dispetcher.message_handler()
@dispetcher.throttled(anti_flood,rate=2)
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
        case "📰Текущие новости":
            choice_rubric(finish_str,"Текущие новости")
            cnt_str = 1
            for news in result_list:
                if cnt_str == 2:
                    res = "🔥 " + title + '\n' + news
                    await message.answer(res)
                    cnt_str = 1
                elif cnt_str == 1:
                    title = news
                    cnt_str+=1
            result_list.clear()
        case "🆕Последняя новость":
            choice_rubric(finish_str,"Последняя новость")

            cnt_str = 1
            for news in result_list:
                if cnt_str == 2:
                    res = title + '\n' + news
                    await message.answer(res)
                    cnt_str = 1
                elif cnt_str == 1:
                    title = news
                    cnt_str+=1
            result_list.clear()
        case "🔙Главное меню":
            await message.answer("🔙Главное меню", reply_markup=kb.main_menu)
        case _:
            await message.answer("Введена неизвестная команда!" +'\n'+ "Попробуйте написать команду: /help")

        

if __name__ == '__main__':
    executor.start_polling(dispetcher,skip_updates=True)