import ScrapeWebsite
import datetime
from ScrapeWebsite import scrape_country

Country = 'USA'
Website = 'https://www.worldometers.info/coronavirus/#countries'
covid_info_dict = scrape_country(Country,Website)
print(covid_info_dict)