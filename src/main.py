import json
import os
import asyncio
from weather_service import Weather
from aiogram import Bot, Dispatcher
from aiogram.types import Message, Update
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
BOT_TOKEN = os.getenv("BOT_TOKEN")

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
DEFAULT_CITY = os.getenv("DEFAULT_CITY", "Samara")
weather_service = WeatherService(WEATHER_API_KEY)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


weather_button = KeyboardButton(text="🌤️ Погода")
keyboard = ReplyKeyboardMarkup(
    keyboard=[[weather_button]],
    resize_keyboard=True
)

   


@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer("Привет!")
    
@dp.message(lambda message: message.text == "🌤️ Погода")
async def weather_button_handler(message: Message):
    await message.answer("🌍 Запрашиваю погоду...")
    weather_info = await weather_service.get_weather()
    await message.answer(weather_info, parse_mode="Markdown")

@dp.message(Command("city"))
async def change_city(message: Message):
    args = message.text.split(maxsplit=1)
    if len(args) > 1:
        new_city = args[1]
        result = weather_service.set_city(new_city)
        await message.answer(result)
    else:
        current_city = weather_service.get_current_city()
        await message.answer(
            f"🏙️ *Изменить город*\n\n"
            "Используй команду:\n"
            "/city Название города\n\n"
            f"*Текущий город:* {current_city}",
            parse_mode="Markdown")

async def handler(event: dict, context):
    body: str = event['body']
    update_data = json.loads(body) if body else {}
    
    
    await dp.feed_update(
        bot,
        Update.model_validate(update_data)
    )
    
    return {"statusCode": 200, "body": "OK"}
    
async def main():
    await dp.start_polling(bot)
    
    
if __name__ == "__main__":
    asyncio.run(main())