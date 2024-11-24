from django.shortcuts import render, redirect
import requests
import json

# Your OpenWeatherMap API key
API_KEY = "3eab6e609ad2c6909fd44c6a6d1a5dac"

from datetime import datetime

def get_weather(city):
    """
    Function to get detailed weather for a given city.
    """
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        weather_data = json.loads(response.text)

        # Extract additional details
        city_name = weather_data.get("name")
        country = weather_data["sys"].get("country")
        temperature = round(weather_data["main"]["temp"] - 273.15, 2)  # Kelvin to Celsius
        description = weather_data["weather"][0].get("description").capitalize()
        humidity = weather_data["main"].get("humidity")
        wind_speed = weather_data["wind"].get("speed")
        pressure = weather_data["main"].get("pressure")
        visibility = weather_data.get("visibility", "N/A")
        
        # Convert sunrise/sunset timestamps to readable format
        sunrise = datetime.utcfromtimestamp(weather_data["sys"].get("sunrise")).strftime('%H:%M:%S')
        sunset = datetime.utcfromtimestamp(weather_data["sys"].get("sunset")).strftime('%H:%M:%S')

        return {
            "city": city_name,
            "country": country,
            "temperature": temperature,
            "description": description,
            "humidity": humidity,
            "wind_speed": wind_speed,
            "pressure": pressure,
            "visibility": visibility,
            "sunrise": sunrise,
            "sunset": sunset,
        }
    else:
        return {"error": "City not found or API error."}





# Django view for the index page
def index(request):
    if request.method == "POST":
        city = request.POST.get("city")
        if city:
            weather = get_weather(city)
            return render(request, 'index.html', {"weather": weather})
    return render(request, 'welcome/index.html')

def weather_details(request):
    if request.method == "POST":
        city = request.POST.get("city")
        if city:
            weather = get_weather(city)  # Fetch formatted weather data
            return render(request, 'welcome/weather_response.html', {"weather": weather})
    return redirect('index')