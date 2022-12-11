import ScrapeWebsite
from ScrapeWebsite import scrape_country
import json
from math import pi
import datetime
from datetime import date
import pandas as pd
import numpy as np
from bokeh.layouts import column, row, gridplot
from bokeh.models import (ColumnDataSource, DataTable, HoverTool, IntEditor,
                          NumberEditor, NumberFormatter, SelectEditor,
                          StringEditor, StringFormatter, TableColumn, CustomJS, MultiChoice)
from bokeh.palettes import HighContrast3, Category20c
from bokeh.transform import cumsum
from bokeh.plotting import figure, show
from bokeh.io import show
from bokeh.palettes import Spectral4
from bokeh.plotting import figure, show
from bokeh.models import LassoSelectTool, Plot, WheelZoomTool


# Scrape the Data
Country = 'New Zealand'
Website = 'https://www.worldometers.info/coronavirus/#countries'
country_covid_info = scrape_country(Country,Website)

# Retreive the Dictionary from the Json
today = str(date.today())
toad = today.split('-')
today = datetime.date(int(toad[0]),int(toad[1]),int(toad[2]))
yesterday = datetime.date(int(toad[0]),int(toad[1]),int(toad[2])-1)
twodays = datetime.date(int(toad[0]),int(toad[1]),int(toad[2])-2)

f1 = open(f'{today}-table.json')
Dictionary = json.load(f1)
f1.close()
f2 = open(f'{yesterday}-table.json')
yesterdayDictionary = json.load(f2)
f2.close()
f3 = open(f'{twodays}-table.json')
twodaysDictionary = json.load(f3)
f3.close()    

Countries = list(Dictionary.keys())
Countries.remove('World')

cds = ColumnDataSource(twodaysDictionary)

tot_cases = []
tot_recov = []
new_cases = []
new_deaths = []
yesterday_cases = []
yesterday_deaths = []
twodays_cases = []
twodays_deaths = []
for m in Countries:
    if Dictionary[m][4] == '':
        Dictionary[m][4] = '0'
    if Dictionary[m][3] == '':
        Dictionary[m][3] = '0'
    if Dictionary[m][1] == '':
        Dictionary[m][1] = '0'
    if yesterdayDictionary[m][3] == '':
        Dictionary[m][3] = '0'
    if yesterdayDictionary[m][1] == '':
        Dictionary[m][1] = '0'
    if twodaysDictionary[m][3] == '':
        Dictionary[m][3] = '0'
    if twodaysDictionary[m][1] == '':
        Dictionary[m][1] = '0'
    tot_cases.append(int(Dictionary[m][0].replace(',','')))
    tot_recov.append(int(Dictionary[m][4].replace(',','').replace('N/A','0')))
    new_cases.append(int(Dictionary[m][1].replace(',','').replace('N/A','0')))
    new_deaths.append(int(Dictionary[m][3].replace(',','')))
    yesterday_cases.append(int(Dictionary[m][1].replace(',','').replace('N/A','0')))
    yesterday_deaths.append(int(Dictionary[m][3].replace(',','')))
    twodays_cases.append(int(Dictionary[m][1].replace(',','').replace('N/A','0')))
    twodays_deaths.append(int(Dictionary[m][3].replace(',','')))

Rates = ["Total Cases", "Recovered Cases"]
                                                    # data with country title, the death cases and the recovered cases
data = {'Countries' : Countries,
        'Total Cases'  : tot_cases,
        'Recovered Cases' : tot_recov}
S = figure(
    x_range=Countries, 
    height=250,
    width= 1250,
    title="Case Results by Country",
    toolbar_location=None,
    tools="hover",
    tooltips="$name @Countries: @$name")
S.add_tools('xwheel_zoom')
S.add_tools('xpan')

S.xaxis.major_label_orientation = np.pi/4
colors = ['#FF0000','#008000']
S.vbar_stack(Rates, x='Countries', width=0.9, color=colors, source=data,
             legend_label=Rates)

source = ColumnDataSource(data=dict(
    #x=[str(twodays), str(yesterday), str(today)],          # I cent seem to get it to work with strings or datetime variables
    x =[1,2,3],
    y1=[twodays_deaths[0],yesterday_deaths[0],new_deaths[0]],
    y2=[twodays_deaths[1],yesterday_deaths[1],new_deaths[1]],
    y3=[twodays_deaths[2],yesterday_deaths[2],new_deaths[2]],
    y4=[twodays_deaths[3],yesterday_deaths[3],new_deaths[3]],
    y5=[twodays_deaths[4],yesterday_deaths[4],new_deaths[4]],
    y6=[twodays_deaths[5],yesterday_deaths[5],new_deaths[5]],
    y7=[twodays_deaths[6],yesterday_deaths[6],new_deaths[6]],
    y8=[twodays_deaths[7],yesterday_deaths[7],new_deaths[7]],
    y9=[twodays_deaths[8],yesterday_deaths[8],new_deaths[8]],
    y10=[twodays_deaths[9],yesterday_deaths[9],new_deaths[9]],# Data for New deaths
))
I = figure(
    width=400,
    height=400, 
    x_axis_label='Date')      # x_axis_type = datetime

ys = ['y1','y2','y3','y4','y5','y6','y7']

I.vline_stack(ys, x='x', source=source, legend_label = ys)
I.legend.title='Markers'
I.legend.location = "top_left"
I.legend.click_policy="hide"


grid = gridplot([[S],[I]])
show(grid)

