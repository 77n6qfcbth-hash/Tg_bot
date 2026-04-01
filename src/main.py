import json
import os
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import CallbackQuery, KeyboardButton, Message, ReplyKeyboardMarkup, Update
from aiogram.filters import Command
from weather import (
    get_weather,
    weather_kb,
    format_weather,
    user_locations
)

BOT_TOKEN =os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()



location_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📍 Отправить геолокацию", request_location=True)]
    ],
    resize_keyboard=True
)
@dp.callback_query(lambda c: c.data == "weather_now")
async def weather_now(callback: CallbackQuery):
    user_id = callback.from_user.id

    if user_id not in user_locations:
        await callback.message.answer(
            "Сначала отправь геолокацию 👇",
            reply_markup=location_kb
        )
        return

    lat, lon = user_locations[user_id]
    data = await get_weather(lat, lon)

    text = format_weather(data)

    await callback.message.answer(text)
    await callback.answer()


#кнопка "локация" 
@dp.callback_query(lambda c: c.data == "weather_location")
async def location_request(callback: CallbackQuery):
    await callback.message.answer(
        "Отправь геолокацию 👇",
        reply_markup=location_kb
    )
    await callback.answer()


#геолокация 
@dp.message()
async def location_handler(message: Message):
    if message.location:
        user_id = message.from_user.id
        lat = message.location.latitude
        lon = message.location.longitude

        user_locations[user_id] = (lat, lon)

        await message.answer(
            "Локация сохранена ✅",
            reply_markup=weather_kb()
        )

    
@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer("Привет!", reply_markup=weather_kb())
    
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