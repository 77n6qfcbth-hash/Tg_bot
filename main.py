import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command

BOT_TOKEN = "8629380981:AAFybFQRSVHBmqyGBNPFcIiuqeeztbl-0TI"
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer("Привет!")
    
async def main():
    await dp.start_polling(bot)
    
    
if __name__ == "__main__":
    asyncio.run(main())