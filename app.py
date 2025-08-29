from flask import Flask, render_template, request
import requests
from api_key import API_KEY
import webbrowser
import threading

app = Flask(__name__)

# Weather API funksiyası
def fetch_weather(city: str):
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    try:
        resp = requests.get(url, params=params, timeout=10)
    except requests.RequestException as e:
        return None, f"Error: request failed ({e})"

    if resp.status_code == 200:
        data = resp.json()
        city_name = data["name"]
        temp = data["main"]["temp"]
        weather_desc = data["weather"][0]["description"]
        return f"Weather in {city_name}: {temp}°C, {weather_desc}", None
    else:
        try:
            err_msg = resp.json().get("message", resp.text)
        except Exception:
            err_msg = resp.text
        return None, f"Error: {resp.status_code} {err_msg}"

@app.route("/", methods=["GET"])
def index():
    city = request.args.get("city", "").strip()
    result, error = (None, None)
    if city:
        result, error = fetch_weather(city)
    return render_template("index.html", city=city, result=result, error=error)

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

if __name__ == "__main__":
    threading.Timer(1.5, open_browser).start()
    app.run(debug=True)
