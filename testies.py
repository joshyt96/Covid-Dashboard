from bokeh.layouts import column
from bokeh.models import (ColumnDataSource, DataTable, HoverTool, IntEditor,
                          NumberEditor, NumberFormatter, SelectEditor,
                          StringEditor, StringFormatter, TableColumn)
from bokeh.plotting import figure, show
import json
from datetime import date
from bokeh.sampledata.autompg2 import autompg2 as mpg


#today = str(date.today())
#f = open(f'{today}-table.json')
#Dictionary = json.load(f)

source = ColumnDataSource(data=mpg)


columns = [
    TableColumn(field="manufacturer", title="Country"),
    TableColumn(field="model", title="Daily Deaths"),
    TableColumn(field="cty", title="Total Deaths"),
    TableColumn(field="hwy", title="Deaths Per Million"),
]
data_table = DataTable(source=source, columns=columns, editable=True, width=800,
                       index_position=-1, index_header="row index", index_width=60)

p = figure(width=800, height=300, tools="pan,wheel_zoom,xbox_select,reset", active_drag="xbox_select")

cty = p.circle(x="index", y="cty", fill_color="#396285", size=8, alpha=0.5, source=source)
hwy = p.circle(x="index", y="hwy", fill_color="#CE603D", size=8, alpha=0.5, source=source)


cty_hover_tool = HoverTool(renderers=[cty])
hwy_hover_tool = HoverTool(renderers=[hwy])

p.add_tools(cty_hover_tool, hwy_hover_tool)

show(column(p, data_table))