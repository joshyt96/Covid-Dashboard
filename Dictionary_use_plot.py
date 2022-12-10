from bokeh.layouts import column
from bokeh.models import (ColumnDataSource, DataTable, HoverTool, IntEditor,
                          NumberEditor, NumberFormatter, SelectEditor,
                          StringEditor, StringFormatter, TableColumn)
from bokeh.plotting import figure, show
from bokeh.sampledata.autompg2 import autompg2 as mpg

mydict = {'key1':[1,2,3,4],'key2':[2,4,6,8]}

cds = ColumnDataSource(mydict)

p = figure(width=800, height=300, tools="pan,wheel_zoom,xbox_select,reset", active_drag="xbox_select")

cty = p.circle(x="key1", y="key2", fill_color="#396285", size=12, alpha=0.5, source=cds)

show(p)