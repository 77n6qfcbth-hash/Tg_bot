from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# главное меню
main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📅 Расписание"),
            KeyboardButton(text="🌤 Погода"),
        ]
    ],
    resize_keyboard=True
)

# меню расписания
schedule_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Сегодня"),
            KeyboardButton(text="Неделя"),
        ],
        [
            KeyboardButton(text="⬅️ Назад"),
        ]
    ],
    resize_keyboard=True
)