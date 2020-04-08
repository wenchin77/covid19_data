from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from datetime import date
import requests

def index(request):
  response = requests.get('https://pomber.github.io/covid19/timeseries.json')
  data = response.json()
  country = 'Australia'
  lastdate = len(data[country])-1

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
    'data': data,
    'dates': dates,
    # 'today': date.today().strftime("%Y-%m-%d"),
    'firstdate': data[country][0]['date'],
    'length': len(data[country])+1,
    'total_confirmed': f'{total_confirmed:,}', # print number with commas for readability
    'total_deaths': f'{total_deaths:,}',
    'total_recovered': f'{total_recovered:,}',
  })
