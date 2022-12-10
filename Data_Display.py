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

# Scrape the Data
Country = 'New Zealand'
Website = 'https://www.worldometers.info/coronavirus/#countries'
country_covid_info = scrape_country(Country,Website)

# Retreive the Dictionary from the Json
today = str(date.today())
toad = today.split('-')
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

# Plot the Static Plot
    # Countries = list(Dictionary.keys())
Countries = ['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries']
Rates = ["Death Cases", "Recovered Cases"]
                                                    # data with country title, the death cases and the recovered cases
data = {'Countries' : Countries,
        'Death Cases'   : [2, 1, 4, 3, 2, 4],
        'Recovered Cases'   : [5, 3, 4, 2, 4, 6]}
S = figure(x_range=Countries, height=250, title="Case Results by Country",
           toolbar_location=None, tools="hover", tooltips="$name @Countries: @$name")
colors = ['#FF0000','#008000']
S.vbar_stack(Rates, x='Countries', width=0.9, color=colors, source=data,
             legend_label=Rates)
#S.x_range.range_padding = 0.1
#S.legend.location = "top_left"
#S.legend.orientation = "horizontal"

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
P = figure(height=350, title="Percent of Cases", toolbar_location=None,
           tools="hover", tooltips="@country: @value%", x_range=(-0.5, 1.0))
P.wedge(x=0, y=1, radius=0.4,
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color='color', legend_field='country', source=data)
P.axis.visible = False
P.grid.grid_line_color = None


# Widget
OPTIONS = list(Dictionary.keys())

W = MultiChoice(value=["foo", "baz"], options=OPTIONS)                      # not sure what value section does
W.js_on_change("value", CustomJS(code="""
    console.log('W: value=' + this.value, this.toString())"""))

# Interactive plot
                                                # We need the plot to somehow incorperate the widget
                                                # I was also thinking about making a dictionary for yesterday and yesterday2
                                                # I already got the tables just didnt deal with json
                                                # See scrape_data_experiments
                                                # Add a legend
source = ColumnDataSource(data=dict(
    x=[1, 2, 3, 4, 5],          # Dictionary for today yesterday and yesterday2
    y1=[1, 2, 4, 3, 4],         # Data for New cases
    y2=[1, 4, 2, 2, 3],         # Data for New deaths
))
I = figure(width=400, height=400)

I.vline_stack(['y1', 'y2'], x='x', source=source)



grid = gridplot([[P,I],[S,W]])
show(grid)

