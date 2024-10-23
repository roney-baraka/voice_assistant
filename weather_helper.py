import requests
import config 

def get_weather(city) :
    api_key = config.OPENWEATHER_API_KEY
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(url).json()


    if response["cod"] == 200:
        weather = response ['weather'][0]['description']
        temp = round(response['main']['temp'] - 273.15, 2) #Kelvin to Celsius
        return f"The weather in {city} with a temperature of {temp}°C."
    else:
        return "Sorry, I couldn't fetch the weather."