import ScrapeWebsite
import json
from datetime import date
import pandas as pd
import numpy as np
from ScrapeWebsite import scrape_country
from bokeh.layouts import column, row
from bokeh.models import (ColumnDataSource, DataTable, HoverTool, IntEditor,
                          NumberEditor, NumberFormatter, SelectEditor,
                          StringEditor, StringFormatter, TableColumn)
from bokeh.palettes import HighContrast3
from bokeh.plotting import figure, show

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

# Turn Keys into a list
keyes = list(Dictionary.keys())
#print(keyes)
#print(range(5))
#for i in range(5):
#    print(keyes[i])


# Plot the Static Plot
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

#S.y_range.start = 0
#S.x_range.range_padding = 0.1
#S.xgrid.grid_line_color = None
#S.axis.minor_tick_line_color = None
#S.outline_line_color = None
#S.legend.location = "top_left"
#S.legend.orientation = "horizontal"

# Interactive plot

show(row(S))        # Temporary till update
# shot(row(I,S))    # Final when interactive is put in

