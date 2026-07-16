from django.shortcuts import render, redirect
from dotenv import load_dotenv
from .functions.time_of_day import find_time
import os

import requests

load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# Create your views here.

def home_view(request):
    return render(request, 'weather_app/home.html')


def current_view(request):
    city = request.GET.get('city')
    unit = request.GET.get('unit', 'imperial')

    if not city:
        return render(request, 'weather_app/home.html')

    url = f'https://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}'
    response = requests.get(url)
    data = response.json()

    #Catches invalid searches
    try:
        current = data['current']
    except KeyError:
        return render(request, 'weather_app/home.html', {"error" : "Invalid city."})
        
    # Gets the acutal proper location name instead of what the user types
    official_city = data['location']['name']
    time = find_time(current['is_day'])

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
            "feels_like": current["feelslike_c"],
            "precipitation": current["precip_mm"],
            "heat_index": current["heatindex_c"],
            "wind_chill": current["windchill_c"],
            "wind_speed": current["wind_kph"],
            "wind_gust": current["gust_kph"],            
            "dew_point": current["dewpoint_c"],
            "visibility": current["vis_km"],
            "pressure": current["pressure_mb"],
            # "wet_bulb": current["wetbulb_c"],
            # "misc" : misc
        }
    else:
        weather = {
            "temperature": current["temp_f"],
            "feels_like": current["feelslike_f"],
            "precipitation": current["precip_in"],
            "heat_index": current["heatindex_f"],
            "wind_chill": current["windchill_f"],
            "wind_speed": current["wind_mph"],
            "wind_gust": current["gust_mph"],            
            "dew_point": current["dewpoint_f"],
            "visibility": current["vis_miles"],
            "pressure": current["pressure_in"],
            # "wet_bulb": current["wetbulb_f"],
            # "misc" : misc
        }

    context = {
        "current" : current,
        "city" : city,
        "weather" : weather,
        "official_city": official_city,
        "unit" : unit,
        "time" : time,
    }
    return render(request, 'weather_app/current.html', context)


def forcast_view(request):

    city = request.GET.get('city')
    unit = request.GET.get('unit', 'imperial')

    if not city:
        return render(request, 'weather_app/home.html')

    url = f'https://api.weatherapi.com/v1/forecast.json?key={WEATHER_API_KEY}&q={city}'
    response = requests.get(url)
    data = response.json()
        
    # Gets the acutal proper location name instead of what the user types
    official_city = data['location']['name']
    forecast = data['forecast']['forecastday'][0]

    context = {
        "city" : city,
        "official_city" : official_city,
        "forecast" : forecast,
        "unit" : unit,
    }
    return render(request, 'weather_app/forecast.html', context)


def specific_view(request):

    city = request.GET.get('city')
    unit = request.GET.get('unit', 'imperial')
    index = int(request.GET.get('index', 0))

    if not city:
        return render(request, 'weather_app/home.html')

    url = f'https://api.weatherapi.com/v1/forecast.json?key={WEATHER_API_KEY}&q={city}'
    response = requests.get(url)
    data = response.json()
        
    # Gets the acutal proper location name instead of what the user types
    official_city = data['location']['name']
    hour = data['forecast']['forecastday'][0]['hour'][index]
    

    context = {
        "city" : city,
        "official_city" : official_city,
        "unit" : unit,
        "hour" : hour,
        "index" : index,
    }
    return render(request, 'weather_app/specific.html', context)