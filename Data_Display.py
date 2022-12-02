import ScrapeWebsite
import datetime
from ScrapeWebsite import scrape_country

Country = 'New Zealand'
Website = 'https://www.worldometers.info/coronavirus/#countries'
country_covid_info = scrape_country(Country,Website)
print(country_covid_info)