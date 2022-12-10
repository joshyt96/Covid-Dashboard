import ScrapeWebsite
import datetime
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
print(country_covid_info)

# Plot the Static Plot
Countries = ['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries']
Rates = ["Death Cases", "Recovered Cases"]

data = {'Countries' : Countries,
        'Death Cases'   : [2, 1, 4, 3, 2, 4],
        #'Reco Cases'   : [5, 3, 4, 2, 4, 6],
        'Recovered Cases'   : [5, 3, 4, 2, 4, 6]}
colors = ['#FF0000','#008000']
S = figure(x_range=Countries, height=250, title="Case Results by Country",
           toolbar_location=None, tools="hover", tooltips="$name @Countries: @$name")

S.vbar_stack(Rates, x='Countries', width=0.9, color=colors, source=data,
             legend_label=Rates)

S.y_range.start = 0
S.x_range.range_padding = 0.1
S.xgrid.grid_line_color = None
S.axis.minor_tick_line_color = None
S.outline_line_color = None
S.legend.location = "top_left"
S.legend.orientation = "horizontal"

# Interactive plot

#show(row(I,S))

