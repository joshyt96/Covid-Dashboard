##################################################################
# Data Table Code
##################################################################

from bokeh.layouts import column
from bokeh.models import (ColumnDataSource, DataTable, HoverTool, IntEditor,
                          NumberEditor, NumberFormatter, SelectEditor,
                          StringEditor, StringFormatter, TableColumn)

from bokeh.plotting import figure, show
from bokeh.sampledata.autompg2 import autompg2 as mpg

source = ColumnDataSource(mpg)

manufacturers = sorted(mpg["manufacturer"].unique())
models = sorted(mpg["model"].unique())
transmissions = sorted(mpg["trans"].unique())
drives = sorted(mpg["drv"].unique())
classes = sorted(mpg["class"].unique())

columns = [
    TableColumn(field="manufacturer", title="Manufacturer"),
    TableColumn(field="model", title="Model"),
    TableColumn(field="displ", title="Displacement"),
    TableColumn(field="year", title="Year"),
    TableColumn(field="cyl", title="Cylinders"),
    TableColumn(field="trans", title="Transmission"),
    TableColumn(field="drv", title="Drive"),
    TableColumn(field="class", title="Class"),
    TableColumn(field="cty", title="City MPG"),
    TableColumn(field="hwy", title="Highway MPG"),
]
data_table = DataTable(source=source, columns=columns, editable=True, width=800,
                       index_position=-1, index_header="row index", index_width=60)

p = figure(width=800, height=300, tools="pan,wheel_zoom,xbox_select,reset", active_drag="xbox_select")

cty = p.circle(x="index", y="cty", fill_color="#396285", size=20, alpha=0.5, source=source)
hwy = p.circle(x="index", y="hwy", fill_color="#CE603D", size=8, alpha=0.5, source=source)

tooltips = [
    ("Manufacturer", "@manufacturer"),
    ("Model", "@model"),
    ("Displacement", "@displ"),
    ("Year", "@year"),
    ("Cylinders", "@cyl"),
    ("Transmission", "@trans"),
    ("Drive", "@drv"),
    ("Class", "@class"),
]
cty_hover_tool = HoverTool(renderers=[cty], tooltips=tooltips + [("City MPG", "@cty")])
hwy_hover_tool = HoverTool(renderers=[hwy], tooltips=tooltips + [("Highway MPG", "@hwy")])

p.add_tools(cty_hover_tool, hwy_hover_tool)

show(column(p, data_table))

