from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from datetime import date
from operator import getitem 
import requests

def index(request):
  response = requests.get('https://pomber.github.io/covid19/timeseries.json')
  data = response.json()
  country = 'Australia'
  lastdate = len(data[country])-1

  latest = dict()
  for country in data:
    latest[country] = {
      'confirmed': data[country][lastdate]['confirmed'],
      'deaths': data[country][lastdate]['deaths'],
      'recovered': data[country][lastdate]['recovered'],
    }
  # Sort nested dictionary by key 
  latest_sorted = dict(sorted(latest.items(), key=lambda x: getitem(x[1], 'confirmed') ,reverse=True))
  # latest_sorted can also use this line below:
  # latest_sorted = {k: v for k, v in sorted(latest.items(), key=lambda x: getitem(x[1], 'confirmed') ,reverse=True)}
  data_sorted = dict(sorted(data.items(), key=lambda country: getitem(country[1][lastdate],'confirmed'), reverse=True))

  dates = dict()
  index = 0
  for x in data[country]:
    datestr = x['date']
    dateobj = datetime.strptime(datestr,"%Y-%m-%d")
    dates[index] = dateobj
    index += 1

  total_confirmed = 0
  total_deaths = 0
  total_recovered = 0
  for country in data:
    total_confirmed += data[country][lastdate]['confirmed']
    total_deaths += data[country][lastdate]['deaths']
    total_recovered += data[country][lastdate]['recovered']
  
  return render(request, 'data/index.html', {
    'date': data[country][lastdate]['date'],
    'data': data_sorted,
    'dates': dates,
    'latest': latest_sorted,
    # 'today': date.today().strftime("%Y-%m-%d"),
    'firstdate': data[country][0]['date'],
    'length': len(data[country])+1,
    'total_confirmed': total_confirmed,
    'total_deaths': total_deaths,
    'total_recovered': total_recovered,
  })
