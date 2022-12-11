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
from bokeh.models import TabPanel, Tabs
from bokeh.plotting import figure, show


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
tot_deaths = []
tot_recov = []
act_case = []
test_1M_pop = []
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
    if Dictionary[m][2] == '':
        Dictionary[m][2] = '0'
    if Dictionary[m][0] == '':
        Dictionary[m][0] = '0'
    if Dictionary[m][6] == '':
        Dictionary[m][6] = '0'
    if Dictionary[m][11] == '':
        Dictionary[m][11] = '0'
    tot_cases.append(int(Dictionary[m][0].replace(',','')))
    #tot_deaths.append(int(Dictionary[m][2].replace(',','').replace('N/A','0')))
    tot_recov.append(int(Dictionary[m][4].replace(',','').replace('N/A','0')))
    act_case.append(int(Dictionary[m][6].replace(',','').replace('N/A','0')))
    test_1M_pop.append(int(Dictionary[m][11].replace(',','').replace('N/A','0')))

Rates = ["Total Cases", "Recovered Cases"]
                                                    # data with country title, the death cases and the recovered cases
data = {'Countries' : Countries,
        'Total Cases'  : tot_cases,
        'Recovered Cases' : tot_recov
        }
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
    y1 = [1,2,3]
))
stat_names = [
    'Total Cases',
    #'Total Deaths',
    'Total Recovered',
    'Active Cases',
    'Test/ 1M Pop'
    ]

USA = figure(
    height=400,
    width = 700,
    x_range = stat_names,
    title="COVID Stats for USA",
    toolbar_location=None,
    tools="hover",
    tooltips="$top @stat_names: @$top"
)
USA.vbar(
    stat_names,
    top=[tot_cases[0],tot_recov[0],act_case[0],test_1M_pop[0]],
    bottom=0,
    width=0.9)
tab1 = TabPanel(child=USA, title="USA")

INDIA = figure(
    height=400,
    width = 700,
    x_range = stat_names,
    title="COVID Stats for USA",
    toolbar_location=None,
    tools="hover",
    tooltips="$name @Countries: @$name"
)
INDIA.vbar(
    stat_names,
    top=[tot_cases[1],tot_recov[1],act_case[1],test_1M_pop[1]],
    bottom=0,
    width=0.9)
tab2 = TabPanel(child=INDIA, title="INDIA")

FRANCE = figure(
    height=400,
    width = 700,
    x_range = stat_names,
    title="COVID Stats for USA",
    toolbar_location=None,
    tools="hover",
    tooltips="$name @Countries: @$name"
)
FRANCE.vbar(
    stat_names,
    top=[tot_cases[2],tot_recov[2],act_case[2],test_1M_pop[2]],
    bottom=0,
    width=0.9)
tab3 = TabPanel(child=FRANCE, title="FRANCE")

GERMANY = figure(
    height=400,
    width = 700,
    x_range = stat_names,
    title="COVID Stats for USA",
    toolbar_location=None,
    tools="hover",
    tooltips="$name @Countries: @$name"
)
GERMANY.vbar(
    stat_names,
    top=[tot_cases[3],tot_recov[3],act_case[3],test_1M_pop[3]],
    bottom=0,
    width=0.9)
tab4 = TabPanel(child=GERMANY, title="GERMANY")

BRAZIL = figure(
    height=400,
    width = 700,
    x_range = stat_names,
    title="COVID Stats for USA",
    toolbar_location=None,
    tools="hover",
    tooltips="$name @Countries: @$name"
)
BRAZIL.vbar(
    stat_names,
    top=[tot_cases[4],tot_recov[4],act_case[4],test_1M_pop[4]],
    bottom=0,
    width=0.9)
tab5 = TabPanel(child=BRAZIL, title="BRAZIL")

SKOREA = figure(
    height=400,
    width = 700,
    x_range = stat_names,
    title="COVID Stats for USA",
    toolbar_location=None,
    tools="hover",
    tooltips="$name @Countries: @$name"
)
SKOREA.vbar(
    stat_names,
    top=[tot_cases[5],tot_recov[5],act_case[5],test_1M_pop[5]],
    bottom=0,
    width=0.9)
tab6 = TabPanel(child=SKOREA, title="S. KOREA")

JAPAN = figure(
    height=400,
    width = 700,
    x_range = stat_names,
    title="COVID Stats for USA",
    toolbar_location=None,
    tools="hover",
    tooltips="$name @Countries: @$name"
)
JAPAN.vbar(
    stat_names,
    top=[tot_cases[6],tot_recov[6],act_case[6],test_1M_pop[6]],
    bottom=0,
    width=0.9)
tab7 = TabPanel(child=JAPAN, title="JAPAN")

ITALY = figure(
    height=400,
    width = 700,
    x_range = stat_names,
    title="COVID Stats for USA",
    toolbar_location=None,
    tools="hover",
    tooltips="$name @Countries: @$name"
)
ITALY.vbar(
    stat_names,
    top=[tot_cases[7],tot_recov[7],act_case[7],test_1M_pop[7]],
    bottom=0,
    width=0.9)
tab8 = TabPanel(child=ITALY, title="ITALY")

UK = figure(
    height=400,
    width = 700,
    x_range = stat_names,
    title="COVID Stats for USA",
    toolbar_location=None,
    tools="hover",
    tooltips="$name @Countries: @$name"
)
UK.vbar(
    stat_names,
    top=[tot_cases[8],tot_recov[8],act_case[8],test_1M_pop[8]],
    bottom=0,
    width=0.9)
tab9 = TabPanel(child=UK, title="UK")

RUSSIA = figure(
    height=400,
    width = 700,
    x_range = stat_names,
    title="COVID Stats for USA",
    toolbar_location=None,
    tools="hover",
    tooltips="$name @Countries: @$name"
)
RUSSIA.vbar(
    stat_names,
    top=[tot_cases[9],tot_recov[9],act_case[9],test_1M_pop[9]],
    bottom=0,
    width=0.9)
tab10 = TabPanel(child=RUSSIA, title="RUSSIA")
tabPlots = Tabs(tabs=[tab1,tab2,tab3,tab4,tab5,tab6,tab7,tab8,tab9,tab10])
grid = gridplot([[S],[tabPlots]])
show(grid)

