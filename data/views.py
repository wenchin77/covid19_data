from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import requests


# def index(request):
#     return HttpResponse("Hello, world. You're at the data index.")


def index(request):
    response = requests.get('https://pomber.github.io/covid19/timeseries.json')
    data = response.json()
    return render(request, 'data/index.html', {
        'date': data,
        # 'confirmed': data['Thailand']
    })
