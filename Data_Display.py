import ScrapeWebsite
from ScrapeWebsite import scrape_country
import json
from math import pi
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
f = open(f'{today}-table.json')
Dictionary = json.load(f)
#f.close()

#print(Dictionary['Europe'])



# Plot the Static Plot
    # Countries = list(Dictionary.keys())
Countries = ['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries']
Rates = ["Death Cases", "Recovered Cases"]

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

W = MultiChoice(value=["foo", "baz"], options=OPTIONS)
W.js_on_change("value", CustomJS(code="""
    console.log('W: value=' + this.value, this.toString())"""))

# Interactive plot




#grid = gridplot([[S,I],[P,W]]) # Widget is the select I is interactve
#show(grid)

