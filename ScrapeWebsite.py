from requests_html import HTMLSession
import json
from datetime import date
URL = 'https://www.worldometers.info/coronavirus/#countries'

def scrape_country(country, website):
    # Scrapes data from the website for all countries, and puts all of the info into a .json file,
    # then searches the .json file for the specified country. The new deaths and cumulative deaths
    # (both raw values and normalized per million people) are stored in a dictionary called "crunchy" 
    s = HTMLSession()
    r = s.get(website)

    table = r.html.find('table')[0]
    # Organizes data into a header and its data
    tableheader = [[c.text for c in row.find('th')[:-1]] for row in table.find('tr')][0]
    tabledata = [[c.text for c in row.find('td')[:-1]] for row in table.find('tr')][1:]
    res = [dict(zip(tableheader,t)) for t in tabledata]
    # Sends the data into a json file with today's date as the title
    today = str(date.today())
    with open(f'{today}.table.json','w') as f:
        json.dump(res,f,indent = 4)
        
    with open(f'{today}.table.json','r') as k:
        data = json.load(k)
        
    for i in range(8,237):
        # find the data for the country of interest
        if data[i]['Country,\nOther'] == country:
            # once we find the country, put the desired info into a dictionary called "crunchy"
            crunchy = {}
            crunchy['Country'] = data[i]['Country,\nOther']
            crunchy['Total Deaths'] = data[i]['Total\nDeaths'].replace(',','')
            crunchy['Population'] = data[i]['Population'].replace(',','')
            pop_mils = float(crunchy['Population'])/1000000
            crunchy['Total Deaths per 1M people'] = float(crunchy['Total Deaths'])/pop_mils
            crunchy['New Deaths'] = data[i]['New\nDeaths'].replace(',','').replace('+','')
            if crunchy['New Deaths'] == '':
                crunchy['New Deaths'] = '0'
            crunchy['New Deaths per 1M people'] = float(crunchy['New Deaths'])/pop_mils
            break
        else:
            pass   
    return crunchy
                
#country.lower()





