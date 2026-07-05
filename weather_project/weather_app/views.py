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
    if not city:
        return render(request, 'weather_app/home.html')

    url = f'https://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}'
    response = requests.get(url)
    data = response.json()

    current = data['current'].items()
    context = {
        'city' : city,
        'current' : current
    }

    return render(request, 'weather_app/city.html', context)