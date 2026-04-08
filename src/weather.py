import datetime
import math
from dotenv import load_dotenv
import requests
import os
load_dotenv()
WEATHER_TOKEN = os.getenv("WEATHER_TOKEN")


def get_weather_text(city_name: str) -> str:
    try:
        response = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&lang=ru&units=metric&appid={WEATHER_TOKEN}"
        )
        data = response.json()
        
        if data.get("cod") != 200:
            return "❌ Город не найден"

        city = data["name"]
        cur_temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]

        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = sunset_timestamp - sunrise_timestamp

        code_to_smile = {
            "Clear": "Ясно ☀️",
            "Clouds": "Облачно ☁️",
            "Rain": "Дождь 🌧",
            "Drizzle": "Дождь 🌧",
            "Thunderstorm": "Гроза ⚡",
            "Snow": "Снег ❄️",
            "Mist": "Туман 🌫"
        }

        weather_description = data["weather"][0]["main"]
        wd = code_to_smile.get(weather_description, "🤷‍♂️")

        return (
            f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
            f"Погода в городе: {city}\n"
            f"Температура: {cur_temp}°C {wd}\n"
            f"Влажность: {humidity}%\n"
            f"Давление: {math.ceil(pressure / 1.333)} мм.рт.ст\n"
            f"Ветер: {wind} м/с\n"
            f"Восход: {sunrise_timestamp}\n"
            f"Закат: {sunset_timestamp}\n"
            f"Длительность дня: {length_of_the_day}"
        )

    except Exception as e:
        print(e)
        return "❌ Ошибка при получении погоды"