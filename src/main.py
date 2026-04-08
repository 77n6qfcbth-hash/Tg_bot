import json
import os
import asyncio
from aiogram import F
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.types import BufferedInputFile, Message,  Update
from aiogram.filters import Command
from keyboards import main_kb, schedule_kb
from image_generate import generate_week_image
from shedule import get_today
from weather import get_weather_text
load_dotenv()
BOT_TOKEN =os.getenv("BOT_TOKEN")
WEATHER_TOKEN =os.getenv("WEATHER_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer("Привет!", reply_markup=main_kb)

@dp.message(F.text == "📅 Расписание")
async def schedule_menu(message: Message):
    await message.answer("Выбери 👇", reply_markup=schedule_kb)
    
@dp.message(F.text == "⬅️ Назад")
async def back_to_main(message: Message):
    await message.answer("Главное меню 👇", reply_markup=main_kb)
    
@dp.message(F.text == "Сегодня")
async def today_button(message: Message):
    await message.answer(get_today())
    
@dp.message(F.text == "Неделя")
async def week_button(message: Message):
    bio = generate_week_image()

    await message.answer_photo(
        BufferedInputFile(bio.getvalue(), filename="week.png")
    )
  
@dp.message(F.text == "🌤 Погода")
async def weather_button(message: Message):
    result = get_weather_text('Самара')
    await message.answer(result)

@dp.message()
async def get_weather(message: Message):
    if message.text in [
        "📅 Расписание", "🌤 Погода",
        "Сегодня", "Неделя", "⬅️ Назад"
    ]:
        return

    city = message.text.strip()
    result = get_weather_text(city)

    await message.answer(result)
    
async def handler(event: dict, context):
    body: str = event['body']
    update_data = json.loads(body) if body else {}
    await dp.feed_update(
        bot,
        Update.model_validate(update_data)
    )
    
    return {"statusCode": 200, "body": "OK"}
    
async def main():
    print("Удаляем webhook...")

    result = await bot.delete_webhook(drop_pending_updates=True)
    print("Webhook удалён:", result)

    print("Запуск polling...")
    await dp.start_polling(bot)
     
if __name__ == "__main__":
    asyncio.run(main())