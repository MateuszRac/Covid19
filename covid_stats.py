# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 16:19:02 2020

@author: Mateusz Rac
"""

from datetime import datetime
from datetime import timedelta

import csv
import urllib
from collections import OrderedDict
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import math

covid = OrderedDict()
covid['countries'] = list()

#get confirmed cases

url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv"
response = urllib.request.urlopen(url).read().decode('utf-8').replace('\n','').split('\r')
cr = csv.reader(response, delimiter=',', quotechar='"')


i = 0
for row in cr:
    
    if i==0:
        covid['dates']=[datetime.strptime(date, '%m/%d/%y').date() for date in row[4:]]
        
    else:
        country = OrderedDict()
        country['province/state'] = row[0]
        country['region/country']= row[1]
        country['confirmed'] = [int(x) for x in row[4:]]
        
        covid['countries'].append(country)
    
    i=i+1



#start index
ifrom = 26

fig, ax = plt.subplots(figsize=[15, 7.5],dpi=90)



plt.grid(b=True, which='both')
plt.title("Cumulative confirmed cases of SARS-CoV-2 infections in Europe", fontsize=15)



#number of days
forecast = 7

countries=['Italy','Germany','France','Spain','Switzerland','Norway','Denmark','Poland']

#countries=['Italy']

for country in countries:
    
    confirmed = [x for x in covid['countries'] if x['region/country']==country][0]
    
    n = len(confirmed['confirmed'])
    
    
    num = 0
    den = 0
    for i in range(0,n-2):
        if confirmed['confirmed'][i] > 0:
            p = confirmed['confirmed'][i+1]/confirmed['confirmed'][i]
            num = num + p* (confirmed['confirmed'][i])
            den = den + (confirmed['confirmed'][i])
    days = []
    
    days.append(covid['dates'][-1])
    
    cases_forecast = []
    cases_forecast.append(confirmed['confirmed'][-1])
    
    ratio = num / den
    
    for i in range(0, forecast):
        days.append((days[-1])+timedelta(days=1))
        cases_forecast.append(cases_forecast[-1]*ratio)
    
    s = plt.plot(covid['dates'][ifrom:],confirmed['confirmed'][ifrom:],label=confirmed['region/country'],linewidth=3,alpha=0.75)
    plt.plot(days,cases_forecast,label=confirmed['region/country']+" (forecast)",color = s[0].get_c(),linewidth=3,linestyle=":",alpha=0.75)

plt.legend()


plt.xlabel('Date')
plt.ylabel('SARS-CoV-2 confirmed cases')
ax.set_yscale('log')


axes = plt.gca()
ymin, ymax = axes.get_ylim()
xmin, xmax = axes.get_xlim()

waterkamr = plt.text(xmax+(xmax-xmin)*0.01,ymin, 'Data sources: WHO, CDC, ECDC, NHC, DXY Agreggated by: John Hopkins CSSE\n',ha='left', va='bottom', fontsize=10, color='black',rotation=90, alpha=0.6)

plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in plt.gca().get_yticks()]) 

ax.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m"))
ax.xaxis.set_minor_formatter(mdates.DateFormatter("%d-%m"))



generatedOn = plt.text(xmin+(xmax-xmin)*0.01,ymax+(ymax-ymin)*0.005, 
                      'Genrated on: '+datetime.now().strftime("%Y-%m-%d %H:%M"),ha='left', va='baseline', fontsize=8, color='black')

