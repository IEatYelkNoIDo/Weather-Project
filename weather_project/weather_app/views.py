from django.shortcuts import render
from dotenv import load_dotenv
import os

import requests

load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
city = "Paris"

# Create your views here.
def home(request):

    url = f'https://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}'
    response = requests.get(url)
    data = response.json()

    current = data['current'].items()
    
    context = {
        'current' : current
    }

    return render(request, 'weather_app/home.html', context)