from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton

but1 =  KeyboardButton("📰Текущие новости")
but2 =  KeyboardButton("🆕Последняя новость")
but_exit   = KeyboardButton("🔙Главное меню")
but_polit  = KeyboardButton("💼Политика")
but_econom = KeyboardButton("📉Экономика")
but_sport  = KeyboardButton("🏋Спорт")
but_crypt  = KeyboardButton("💶Бизнес")
but_society  = KeyboardButton("🧑‍🤝‍🧑Общество")


main_menu  = ReplyKeyboardMarkup(resize_keyboard=True).insert(but_polit).insert(but_econom).insert(but_sport).insert(but_crypt).insert(but_society)
other_menu = ReplyKeyboardMarkup(resize_keyboard=True).insert(but1).insert(but2).add(but_exit)