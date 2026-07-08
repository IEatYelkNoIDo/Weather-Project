from django.shortcuts import render, redirect
from dotenv import load_dotenv
import os

import requests

load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# Create your views here.

def home_view(request):
    
    return render(request, 'weather_app/home.html')

def city_view(request):

    city = request.GET.get('city')
    unit = request.GET.get('unit', 'imperial')

    if not city:
        return render(request, 'weather_app/home.html')

    url = f'https://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}'
    response = requests.get(url)
    data = response.json()

    current = data['current']

    misc = {
        "last_updated"   : current['last_updated'],
        "is_day"         : current['is_day'],
        "wind_degree"    : current['wind_degree'],
        "wind_direction" : current['wind_dir'],
        "humidity"       : current['humidity'],
        "cloud"          : current['cloud'],
        "uv"             : current['uv'],
        "will_rain"      : current['will_it_rain'],
        "rain_chance"    : current['chance_of_rain'],
        "will_snow"      : current['will_it_snow'],
        "snow_chance"    : current['chance_of_snow'],
        "short_rad"      : current['short_rad'],
        "diff_rad"       : current['diff_rad'],
        "dni"            : current['dni'],
        "gti"            : current['gti'],
    }

    if unit == "metric":
        weather = {
            "temperature": current["temp_c"],
            "wind_speed": current["wind_kph"],
            "pressure": current["pressure_mb"],
            "precipitation": current["precip_mm"],
            "feels_like": current["feelslike_c"],
            "wind_chill": current["windchill_c"],
            "heat_index": current["heatindex_c"],
            "dew_point": current["dewpoint_c"],
            "visibility": current["vis_km"],
            "wind_gust": current["gust_kph"],
            # "wet_bulb": current["wetbulb_c"],
            # "misc" : misc
        }
    else:
        weather = {
            "temperature": current["temp_f"],
            "wind_speed": current["wind_mph"],
            "pressure": current["pressure_in"],
            "precipitation": current["precip_in"],
            "feels_like": current["feelslike_f"],
            "wind_chill": current["windchill_f"],
            "heat_index": current["heatindex_f"],
            "dew_point": current["dewpoint_f"],
            "visibility": current["vis_miles"],
            "wind_gust": current["gust_mph"],
            # "wet_bulb": current["wetbulb_f"],
            # "misc" : misc
        }

    context = {
        "city" : city,
        "weather" : weather,
    }

    return render(request, 'weather_app/city.html', context)