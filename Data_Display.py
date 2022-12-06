import ScrapeWebsite
import datetime
import pandas as pd
import numpy as np
from ScrapeWebsite import scrape_country

Country = 'New Zealand'
Website = 'https://www.worldometers.info/coronavirus/#countries'
country_covid_info = scrape_country(Country,Website)
print(country_covid_info)