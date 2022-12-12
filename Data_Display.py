from ScrapeWebsite import scrape_country
import json
from math import pi
import datetime
from datetime import date
import numpy as np
from bokeh.layouts import gridplot
from bokeh.models import (ColumnDataSource, TabPanel, Tabs)
from bokeh.palettes import HighContrast3, Category20c
from bokeh.transform import dodge 
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

# Retreive the dictionaries for previous days of data
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

#Seperate data in teh dictionaries in to smaller lists to be used in different plots
tot_cases = []
tot_deaths = []
tot_recov = []
act_case = []
test_1M_pop = []
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
        'TotalCases'  : tot_cases,
        'RecoveredCases' : tot_recov
        }

# Code that makes the bar graph displaying a small amount of data for the entire world
TOOLTIPS = [("Country","@Countries"), 
            ("Total Cases","@TotalCases"),
            ("Recovered Cases","@RecoveredCases")]

B = figure(
    x_range=Countries, 
    height=250,
    width= 1250,
    title="Case Results by Country",
    toolbar_location=None,
    tools="hover",
    tooltips = TOOLTIPS)

B.xaxis.major_label_orientation = np.pi/4
colors = ['#FF0000','#008000']

B.vbar(x=dodge('Countries', -0.22, range=B.x_range), top='TotalCases', color = '#FF0000', source=data,
       width=0.4, legend_label="Total Cases")

B.vbar(x=dodge('Countries',  0.22,  range=B.x_range), top='RecoveredCases', color = '#008000',source=data,
       width=0.4, legend_label="Recovered Cases")

B.add_tools('xwheel_zoom')
B.add_tools('xpan')

# Formatting another dictionary for the next plot
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
    active.append(int(Dictionary[m][6].replace(',','').replace('N/A','0')))
    
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

# Initializing the elements used for top ten plot
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

stat_names = [
    'Total Cases',
    #'Total Deaths',
    'Total Recovered',
    'Active Cases',
    'Test/ 1M Pop'
    ]

# Initializing the elements used for the tabed plots
USA = figure(
    height=400,
    width = 700,
    x_range = stat_names,
    title="COVID Stats for USA",
    toolbar_location=None,
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
    title="COVID Stats for India",
    toolbar_location=None,
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
    title="COVID Stats for France",
    toolbar_location=None,
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
    title="COVID Stats for Germany",
    toolbar_location=None,
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
    title="COVID Stats for Brazil",
    toolbar_location=None,
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
    title="COVID Stats for South Korea",
    toolbar_location=None,
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
    title="COVID Stats for Japan",
    toolbar_location=None,
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
    title="COVID Stats for Italy",
    toolbar_location=None,
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
    title="COVID Stats for UK",
    toolbar_location=None,
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
    title="COVID Stats for Russia",
    toolbar_location=None,
)
RUSSIA.vbar(
    stat_names,
    top=[tot_cases[9],tot_recov[9],act_case[9],test_1M_pop[9]],
    bottom=0,
    width=0.9)
tab10 = TabPanel(child=RUSSIA, title="RUSSIA")
tabPlots = Tabs(tabs=[tab1,tab2,tab3,tab4,tab5,tab6,tab7,tab8,tab9,tab10])



# Time Plot
new_cases = []
yesterday_new_cases = []
twodays_new_cases = []
i = 0

for m in country10:
    if Dictionary[m][1] == '':
        Dictionary[m][1] = '0'
    new_cases.append(int(Dictionary[m][1].replace(',','')))
    if yesterdayDictionary[m][1] == '':
        yesterdayDictionary[m][1] = '0'
    yesterday_new_cases.append(int(yesterdayDictionary[m][1].replace(',','')))
    if twodaysDictionary[m][1] == '':
        twodaysDictionary[m][1] = '0'
    twodays_new_cases.append(int(twodaysDictionary[m][1].replace(',','')))
    print(m)
    
label=[str(twodays), str(yesterday), str(today)]
source = ColumnDataSource(data=dict(
    x =[.5, 1.5, 2.5],
    India =[new_cases[1],yesterday_new_cases[1],twodays_new_cases[1]],
    France =[new_cases[2],yesterday_new_cases[2],twodays_new_cases[2]],
    Germany =[new_cases[3],yesterday_new_cases[3],twodays_new_cases[3]],
    Brazil =[new_cases[4],yesterday_new_cases[4],twodays_new_cases[4]],
    S_Korea =[new_cases[5],yesterday_new_cases[5],twodays_new_cases[5]],
    Japan =[new_cases[6],yesterday_new_cases[6],twodays_new_cases[6]],
    Italy =[new_cases[7],yesterday_new_cases[7],twodays_new_cases[7]],
    UK =[new_cases[8],yesterday_new_cases[8],twodays_new_cases[8]],
    Russia =[new_cases[9],yesterday_new_cases[9],twodays_new_cases[9]],
    USA =[new_cases[0],yesterday_new_cases[0],twodays_new_cases[0]]))
print(country10)

#TColors = ['#5FB3F9','#7ED085','#FEFF00','#FF8D00','#EA5000','#F87E7D','#991310','#000000','#974C00','#9210AD']
T = figure(x_range=label, x_axis_label='Date',
    title="New Cases Results by Country",
    toolbar_location=None,
    tools="hover",
    tooltips="$name @Countries: @$name")  

T.vline_stack(['USA','India','France','Germany','Brazil','S_Korea','Japan','Italy','UK','Russia'], x='x', 
    legend_label=country10,
    #line_color=TColors,
    source=source)
#T.legend.orientation = "horizontal"
#T.legend.location = "top_right"

grid = gridplot([[B],[S],[tabPlots],[T]])
show(grid)

