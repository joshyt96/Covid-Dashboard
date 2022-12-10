##################################################################
# Multi Choice code
##################################################################
from bokeh.io import show
from bokeh.models import CustomJS, MultiChoice
import json
from datetime import date

today = str(date.today())

#Load today's country data
f = open('2022-12-08-table.json')
todayCountryData = json.load(f)
#Make a list of all the country names
countryOptions = list(todayCountryData.keys())

multi_choice = MultiChoice(value=['USA','S. Korea'], options=countryOptions)
multi_choice.js_on_change("value", CustomJS(code="""
    console.log('multi_choice: value=' + this.value, this.toString())"""))

show(multi_choice)