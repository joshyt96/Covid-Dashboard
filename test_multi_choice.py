##################################################################
# Multi Choice code
##################################################################
from bokeh.io import show
from bokeh.models import CustomJS, MultiChoice

OPTIONS = ["foo", "bar", "baz", "quux","ab","b","ff","fe","ji","wr","we","ef","fffff","shittttt","fuk"]

multi_choice = MultiChoice(value=["foo", "baz"], options=OPTIONS)
multi_choice.js_on_change("value", CustomJS(code="""
    console.log('multi_choice: value=' + this.value, this.toString())"""))

show(multi_choice)