from bokeh.layouts import column, row
from bokeh.models import (ColumnDataSource, DataTable, HoverTool, IntEditor,
                          NumberEditor, NumberFormatter, SelectEditor,
                          StringEditor, StringFormatter, TableColumn)
from bokeh.plotting import figure, show
from bokeh.sampledata.autompg2 import autompg2 as mpg
from datetime import date
import json

today = str(date.today())
with open(f'{today}-table.json','r') as k:
    data = json.load(k)

countries = ['USA','India','Germany','Brazil']

tot_death = []
tot_recov = []
for m in countries:
    tot_death.append(int(data[m][2].replace(',','')))
    tot_recov.append(int(data[m][4].replace(',','')))

print(tot_death)

#mydict = {'key1':[1,2,3,4],'key2':[2,4,6,8]}

#cds = ColumnDataSource(mydict)

#p = figure(width=800, height=300, tools="pan,wheel_zoom,xbox_select,reset", active_drag="xbox_select")

#cty = p.circle(x="key1", y="key2", fill_color="#396285", size=12, alpha=0.5, source=cds)

#show(p)


# Plot the Static Plot
Rates = ["Death Cases", "Recovered Cases"]

data = {'Countries' : countries,
        'Death Cases'   : tot_death,
        'Recovered Cases'   : tot_recov}
S = figure(x_range=countries, height=250, title="Case Results by Country",
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

