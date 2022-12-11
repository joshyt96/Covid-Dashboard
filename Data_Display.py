import ScrapeWebsite
from ScrapeWebsite import scrape_country
import json
from math import pi
import datetime
from datetime import date
import pandas as pd
import numpy as np
from bokeh.layouts import column, row, gridplot
from bokeh.models import (ColumnDataSource, FactorRange, DataTable, HoverTool, IntEditor,
                          NumberEditor, NumberFormatter, SelectEditor,
                          StringEditor, StringFormatter, TableColumn, CustomJS, MultiChoice)
from bokeh.palettes import HighContrast3, Category20c
from bokeh.transform import cumsum, dodge 
from bokeh.plotting import figure, show
from bokeh.io import show

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

country10 = Countries[0:10]
tot_cases = []
tot_recov = []
tot_death = []
active = []
for m in country10:
    if Dictionary[m][4] == '':
        Dictionary[m][4] = '0'
    tot_cases.append(int(Dictionary[m][0].replace(',','')))
    tot_recov.append(int(Dictionary[m][4].replace(',','').replace('N/A','0')))
    tot_death.append(int(Dictionary[m][2].replace(',','')))
    active.append(int(Dictionary[m][6].replace(',','')))
    
datachoices = ['Total Cases', 'Recovered Cases','Active Cases','Total Deaths']

data = {'Country' : country10,
         'TotalCases' : tot_cases,
         'RecoveredCases' : tot_recov,
         'ActiveCases' : active,
         'TotalDeaths' : tot_death}
source = ColumnDataSource(data=data)

TOOLTIPS = [("Country","@Country"), 
            ("Total Cases","@TotalCases"),
            ("Recovered Cases","@RecoveredCases"),
            ("Active Cases","@ActiveCases"),
            ("Total Deaths","@TotalDeaths")]

S = figure(x_range=country10, 
           title="Top 10 Countries: click on legend entries to hide the corresponding data",
           height=350, toolbar_location=None, tools="hover", tooltips = TOOLTIPS)

S.vbar(x=dodge('Country', -0.3, range=S.x_range), top='TotalCases', source=source,
       width=0.15, color="#c9d9d3", legend_label="Total Cases")

S.vbar(x=dodge('Country',  -0.1,  range=S.x_range), top='RecoveredCases', source=source,
       width=0.15, color="#718dbf", legend_label="Recovered Cases")

S.vbar(x=dodge('Country',  0.1,  range=S.x_range), top='ActiveCases', source=source,
       width=0.15, color="#1252B3", legend_label="Active Cases")

S.vbar(x=dodge('Country', 0.3, range=S.x_range), top='TotalDeaths', source=source,
       width=0.15, color="#e84d60", legend_label="Total Deaths")

S.x_range.range_padding = 0.05
S.xgrid.grid_line_color = None
S.legend.orientation = "horizontal"
S.legend.location = "top_right"
S.legend.click_policy="hide"

#Rates = ["Total Cases", "Recovered Cases"]
                                                    # data with country title, the death cases and the recovered cases
#data = {'Countries' : Countries,
#        'Total Cases'  : tot_cases,
#        'Recovered Cases' : tot_recov}
#S = figure(x_range=Countries, height=250, width=1000, title="Case Results by Country",
#           toolbar_location=None, tools="hover", tooltips="$name @Countries: @$name")
#S.xaxis.major_label_orientation = np.pi/4
#colors = ['#FF0000','#008000']
#S.vbar_stack(Rates, x='Countries', width=0.9, color=colors, source=data,
#             legend_label=Rates)

# Pie graph
                                                    #  x = Dictionary with just country and the percent of the cases
x = {
    'United States': 157,
    'United Kingdom': 93,
    'Japan': 89,
    'China': 63,
    'Germany': 44,
    'India': 42,
    'Italy': 40,
    'Australia': 35,
    'Brazil': 32,
    'France': 31,
    'Taiwan': 31,
    'Spain': 29
}
data = pd.Series(x).reset_index(name='value').rename(columns={'index': 'country'})
data['angle'] = data['value']/data['value'].sum() * 2*pi
data['color'] = Category20c[len(x)]
P = figure(height=400, title="Percent of Cases", toolbar_location=None,
           tools="hover", tooltips="@country: @value%", x_range=(-0.5, 1.0))
P.wedge(x=0, y=1, radius=0.4,
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color='color', legend_field='country', source=data)
P.axis.visible = False
P.grid.grid_line_color = None


# Interactive plot
                                                # We need the plot to somehow incorporate the widget
                                                # I was also thinking about making a dictionary for yesterday and yesterday2
                                                # I already got the tables just didnt deal with json
                                                # See scrape_data_experiments
                                                # Add a legend

source = ColumnDataSource(data=dict(
    #x=[str(twodays), str(yesterday), str(today)],          # I cent seem to get it to work with strings or datetime variables
    x =[0, 1, 2],
    y1=[1, 2, 4],         # Data for New cases
    y2=[1, 4, 2],         # Data for New deaths
))
I = figure(width=400, height=400, x_axis_label='Date')      # x_axis_type = datetime

I.vline_stack(['y1', 'y2'], x='x', source=source)
#show(I)

W = figure(width=400, height=400, x_axis_label='Date')      # x_axis_type = datetime


grid = gridplot([[P,I],[S,W]])
show(grid)

