import requests
from api_key import API_KEY

CITY = input("Add city: ")

URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

response = requests.get(URL)

if response.status_code == 200:
    data = response.json()
    city = data["name"]
    temp = data["main"]["temp"]
    weather = data["weather"][0]["description"]
    print(f"Weather in {city}: {temp}°C, {weather}")
else:
    print("Error:", response.status_code, response.text)
