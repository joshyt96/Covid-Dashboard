import json
from math import pi
import datetime
from datetime import date
from bokeh.layouts import column, row, gridplot
from bokeh.models import (ColumnDataSource, TabPanel, Tabs, FactorRange, DataTable, HoverTool, IntEditor,
                          NumberEditor, NumberFormatter, SelectEditor,
                          StringEditor, StringFormatter, TableColumn, CustomJS, MultiChoice)
from bokeh.palettes import HighContrast3, Category20c
from bokeh.transform import cumsum, dodge 
from bokeh.plotting import figure, show
from bokeh.io import sho


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
x =[.5, 1.5, 2.5],
India =[new_cases[1],yesterday_new_cases[1],twodays_new_cases[1]],
France =[new_cases[2],yesterday_new_cases[2],twodays_new_cases[2]],
Germany =[new_cases[3],yesterday_new_cases[3],twodays_new_cases[3]],
Brazil =[new_cases[4],yesterday_new_cases[4],twodays_new_cases[4]],
S_Korea=[new_cases[5],yesterday_new_cases[5],twodays_new_cases[5]],
Japan =[new_cases[6],yesterday_new_cases[6],twodays_new_cases[6]],
Italy =[new_cases[7],yesterday_new_cases[7],twodays_new_cases[7]],
UK =[new_cases[8],yesterday_new_cases[8],twodays_new_cases[8]],
Russia =[new_cases[9],yesterday_new_cases[9],twodays_new_cases[9]],
USA =[new_cases[0],yesterday_new_cases[0],twodays_new_cases[0]]

T = figure(x_range=label, x_axis_label='Date',
    title="New Cases Results by Country",
    toolbar_location=None,
    tools="hover",
    tooltips="$name @Countries: @$name")  
T.circle(x, India, legend_label="India",line_color="green")
T.line(x, India, legend_label="India",line_color="green")

T.circle(x, France, legend_label="France",line_color="red")
T.line(x, France, legend_label="France",line_color="red")

T.circle(x, Germany, legend_label="Germany",line_color="orange")
T.line(x, Germany, legend_label="Germany",line_color="orange")

T.circle(x, Brazil, legend_label="Brazil",line_color="blue")
T.line(x, Brazil, legend_label="Brazil",line_color="blue")

T.circle(x, S_Korea, legend_label="S. Korea")
T.line(x, S_Korea, legend_label="S. Korea")

T.circle(x, Japan, legend_label="Japan")
T.line(x, Japan, legend_label="Japan")

T.circle(x, Italy, legend_label="Italy")
T.line(x, Italy, legend_label="Italy")

T.circle(x, UK, legend_label="UK")
T.line(x, UK, legend_label="UK")

T.circle(x, Russia, legend_label="Russia")
T.line(x, Russia, legend_label="Russia")

T.circle(x, USA, legend_label="USA")
T.line(x, USA, legend_label="USA")
show(T)
