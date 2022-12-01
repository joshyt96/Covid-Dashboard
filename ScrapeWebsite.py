import requests
from bs4 import BeautifulSoup 
import json
import pandas as pd
from datetime import date

# Create an URL object, used to make a page object
#reate object page
def scrape_country(url,country):
    page = requests.get(url)

    # Use lxml to make the HTML in a Python ready format
    soup = BeautifulSoup(page.text, 'lxml')

    #Pulls the table that tracks todays COVID data
    table1 = soup.find('table', id='main_table_countries_today')

    # Obtain every title of columns with tag <th>
    headers = []
    for i in table1.find_all('th'):
        title = i.text
        headers.append(title)
 
    # Convert wrapped text in column 13 into one line text
    headers[13] = 'Tests/1M pop'

    # Create a Pandas dataframe
    mydata = pd.DataFrame(columns = headers)

    # Create a for loop to fill mydata
    for j in table1.find_all('tr')[1:]:
        row_data = j.find_all('td')
        row = [i.text for i in row_data]
        length = len(mydata)
        mydata.loc[length] = row

    # Drop and clearing unnecessary rows
    mydata.drop(mydata.index[0:7], inplace=True)
    mydata.drop(mydata.index[222:229], inplace=True)
    mydata.reset_index(inplace=True, drop=True)
    # Drop “#” column
    mydata.drop('#', inplace=True, axis=1)

    #Trim down the dataframe to only columns we need for the project
    wantedDataDF = mydata.iloc[:224]

    #Convert the dataframe to a dictionary with the country name set for keys
    dataDict = wantedDataDF.set_index('Country,Other').T.to_dict('list')

    # Take the created dictionary and save it as a .json file with today's date
    today = str(date.today())
    with open(f'{today}.table.json','w') as f:
        json.dump(dataDict,f)
        
    countryData = dataDict[country]
    totalDeaths = int(countryData[2].replace(',',''))/1000000
    #totalDeaths = int(totalDeathsStr)/1000000
    newDeaths = countryData[3].replace('x','')
    
    print(country + "\n" + "Total deaths (Per 1 Million):" + str(totalDeaths))
    print("Reported deaths today (" + today + '):' + newDeaths)
    
scrape_country('https://www.worldometers.info/coronavirus/#countries','USA')