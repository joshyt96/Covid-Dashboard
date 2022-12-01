import requests
from bs4 import BeautifulSoup 

sauce = requests.get('https://www.worldometers.info/coronavirus/#countries')
soup = BeautifulSoup(sauce.text, 'html.parser')
tables = soup.find_all('table')
with open('csvfile.csv','w') as csv:
    for row in tables[0].find_all('tr')[8:239]:
        line = ""
        for td in row.find_all(['td', 'th']):
            line += '"' + td.text + '",'
        csv.write(line + '\n')

