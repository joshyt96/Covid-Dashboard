import ScrapeWebsite
import pandas as pd
import numpy as np
from ScrapeWebsite import scrape_country
import json
from datetime import date




Country = 'New Zealand'
Website = 'https://www.worldometers.info/coronavirus/#countries'
country_covid_info = scrape_country(Country,Website)


# Retreive the Dictionary from the Json
today = str(date.today())
f = open(f'{today}-table.json')
Dictionary = json.load(f)
#f.close()

# Turn Keys into a list
keyes = list(Dictionary.keys())
print(keyes[5])



