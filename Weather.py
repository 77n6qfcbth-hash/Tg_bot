import aiohttp

class WeatherService: 
    def __init__(self, api_key: str, default_city: str = "Samara"):
        self.api_key = api_key
        self.default_city = default_city
        self.current_city = default_city  
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
        
        
        
    def set_city(self, city: str) -> str:
        self.current_city = city
        return f"✅ Город изменен на: {city}"
    
    def get_current_city(self) -> str:
        return self.current_city
    
    async def get_weather(self, city: str) -> str:
        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'metric',
            'lang': 'ru'
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.base_url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._format_weather(data, city)
                    elif response.status == 404:
                        return f"Город '{city}' не найден"
                    else:
                        return f"Ошибка API. Код: {response.status}"
        except Exception as e:
            return f" Ошибка соединения: {str(e)}"
    
    def _format_weather(self, data: dict, city: str) -> str:
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        wind = data['wind']['speed']
        description = data['weather'][0]['description']
        
        weather_type = data['weather'][0]['main'].lower()
        emoji_map = {
            'clear': '☀️',
            'clouds': '☁️',
            'rain': '🌧️',
            'drizzle': '🌦️',
            'thunderstorm': '⛈️',
            'snow': '❄️',
            'mist': '🌫️',
            'fog': '🌫️'
        }
        emoji = emoji_map.get(weather_type, '🌡️')
        
        return (
            f"{emoji} *Погода в {city}*\n\n"
            f"🌡️ Температура: {temp}°C\n"
            f"🤔 Ощущается как: {feels_like}°C\n"
            f"☁️ {description.capitalize()}\n"
            f"💧 Влажность: {humidity}%\n"
            f"💨 Ветер: {wind} м/с"
        )