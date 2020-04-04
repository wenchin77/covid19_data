from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
import requests

def index(request):
  response = requests.get('https://pomber.github.io/covid19/timeseries.json')
  data = response.json()
  country = 'Australia'
  lastdate = len(data[country])-1
  return render(request, 'data/index.html', {
    'date': data[country][lastdate]['date'],
    'data': data,
  })
