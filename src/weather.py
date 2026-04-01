import aiohttp
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
user_locations = {}
async def get_weather(lat: float, lon: float):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": True
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            data = await resp.json()
            return data.get("current_weather")


def weather_text(code: int):
    match code:
        case 0:
            return "Ясно ☀️"

        case 1 | 2 | 3:
            return "Облачно ☁️"

        case c if 45 <= c <= 48:
            return "Туман 🌫"

        case c if 51 <= c <= 67:
            return "Дождь 🌧"

        case c if 71 <= c <= 77:
            return "Снег ❄️"

        case c if c >= 95:
            return "Гроза ⛈"

        case _:
            return "Неизвестно 🤷"


def weather_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🌤 Сейчас", callback_data="weather_now"),
            InlineKeyboardButton(text="📅 Прогноз", callback_data="weather_forecast")
        ],
        [
            InlineKeyboardButton(text="📍 Обновить локацию", callback_data="weather_location")
        ]
    ])

def format_weather(data):
    return f"""🌤 Сейчас
        🌡 {data['temperature']}°C
        💨 Ветер: {data['windspeed']} км/ч
        ☁️ {weather_text(data['weathercode'])}"""