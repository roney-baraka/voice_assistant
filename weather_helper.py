import requests
import config  

def get_weather(city):
    api_key = config.WEATHER_API_KEY
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    response = requests.get(base_url)
    data = response.json()

    if data["cod"] != "404":
        weather_desc = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        return f"The weather in {city} is {weather_desc} with a temperature of {temp}°C."
    else:
        return "Sorry, I couldn't find the weather for that city."
