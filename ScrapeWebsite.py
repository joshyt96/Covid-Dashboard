from requests_html import HTMLSession
import json
from datetime import date
URL = 'https://www.worldometers.info/coronavirus/#countries'

#def scrape_country(country, website):
    # Scrapes data for all countries
s = HTMLSession()
r = s.get(URL)
table = r.html.find('table')[0]
# Organizes data into a header and its data
tableheader = [[c.text for c in row.find('th')[:-1]] for row in table.find('tr')][0]
tabledata = [[c.text for c in row.find('td')[:-1]] for row in table.find('tr')][1:]
res = [dict(zip(tableheader,t)) for t in tabledata]
# Sends the data into a json file with today's date as the title
today = str(date.today())
with open(f'{today}.table.json','w') as f:
    json.dump(res,f)
#country.lower()






