import os
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer("Привет!")
    
async def handler(event: dict, context):
    print(f"Received event: {event}")
    print(f"Received context: {context}")
    
    return {"statusCode": 200, "body": "OK"}
    
async def main():
    await dp.start_polling(bot)
    
    
if __name__ == "__main__":
    asyncio.run(main())