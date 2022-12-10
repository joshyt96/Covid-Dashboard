import requests
from bs4 import BeautifulSoup 
import json
import pandas as pd
from datetime import date
import datetime


# Create an URL object, used to make a page object
#reate object page
def scrape_country(country,url):
    page = requests.get(url)

    # Use lxml to make the HTML in a Python ready format
    soup = BeautifulSoup(page.text, 'lxml')

    #Pulls the table that tracks todays COVID data
    table1 = soup.find('table', id='main_table_countries_today')
    table2 = soup.find('table', id='main_table_countries_yesterday')
    table3 = soup.find('table', id='main_table_countries_yesterday2')
    
    # Obtain every title of columns with tag <th>
    headers1 = []
    headers2 = []
    headers3 = []
    for i in table1.find_all('th'):
        title1 = i.text
        headers1.append(title1)
    for i in table2.find_all('th'):
        title2 = i.text
        headers2.append(title2)
    for i in table3.find_all('th'):
        title3 = i.text
        headers3.append(title3)
 
    # Convert wrapped text in column 13 into one line text
    headers1[13] = 'Tests/1M pop'
    headers2[13] = 'Tests/1M pop'
    headers3[13] = 'Tests/1M pop'

    # Create a Pandas dataframe
    mydata1 = pd.DataFrame(columns = headers1)
    mydata2 = pd.DataFrame(columns = headers2)
    mydata3 = pd.DataFrame(columns = headers3)

    # Create a for loop to fill mydata
    for j in table1.find_all('tr')[1:]:
        row_data1 = j.find_all('td')
        row1 = [i.text for i in row_data1]
        length1 = len(mydata1)
        mydata1.loc[length1] = row1
    for j in table2.find_all('tr')[1:]:
        row_data2 = j.find_all('td')
        row2 = [i.text for i in row_data2]
        length2 = len(mydata2)
        mydata2.loc[length2] = row2
    for j in table3.find_all('tr')[1:]:
        row_data3 = j.find_all('td')
        row3 = [i.text for i in row_data3]
        length3 = len(mydata3)
        mydata3.loc[length3] = row3
    # Drop and clearing unnecessary rows
    mydata1.drop(mydata1.index[0:7], inplace=True)
    mydata1.drop(mydata1.index[222:229], inplace=True)
    mydata1.reset_index(inplace=True, drop=True)
    mydata2.drop(mydata2.index[0:7], inplace=True)
    mydata2.drop(mydata2.index[222:229], inplace=True)
    mydata2.reset_index(inplace=True, drop=True)
    mydata3.drop(mydata3.index[0:7], inplace=True)
    mydata3.drop(mydata3.index[222:229], inplace=True)
    mydata3.reset_index(inplace=True, drop=True)
    # Drop “#” column
    mydata1.drop('#', inplace=True, axis=1)
    mydata2.drop('#', inplace=True, axis=1)
    mydata3.drop('#', inplace=True, axis=1)

    #Trim down the dataframe to only columns we need for the project
    wantedDataDF1 = mydata1.iloc[:224]
    wantedDataDF2 = mydata2.iloc[:224]
    wantedDataDF3 = mydata3.iloc[:224]

    #Convert the dataframe to a dictionary with the country name set for keys
    dataDict1 = wantedDataDF1.set_index('Country,Other').T.to_dict('list')
    dataDict2 = wantedDataDF2.set_index('Country,Other').T.to_dict('list')
    dataDict3 = wantedDataDF3.set_index('Country,Other').T.to_dict('list')

     # Take the created dictionary and save it as a .json file with today's date
    today = str(date.today())
    toad = today.split('-')
    yesterday = datetime.date(int(toad[0]),int(toad[1]),int(toad[2])-1)
    twodays = datetime.date(int(toad[0]),int(toad[1]),int(toad[2])-2)
    
    with open(f'{today}-table.json','w') as f:
        json.dump(dataDict1,f)
    with open(f'{yesterday}-table.json','w') as f:
        json.dump(dataDict2,f)    
    with open(f'{twodays}-table.json','w') as f:
        json.dump(dataDict3,f)
        
    countryData1 = dataDict1[country]
    countryData2 = dataDict2[country]
    countryData3 = dataDict3[country]
    
    popMil = int(countryData1[12].replace(',',''))/1000000
    totalDeaths = int(countryData1[2].replace(',',''))
    if countryData1[3] == '':
        newDeaths = 0
    else:
        newDeaths = int(countryData1[3].replace('+',''))
    totalDeathsPerMil = totalDeaths/popMil
    newDeathsPerMil = newDeaths/popMil
    # create a list called countryInfo, which contains these elements in this order:
    # [cumulative deaths, cumulative deaths per million, new deaths today, new deaths today per million]
    countryInfo = [totalDeaths, totalDeathsPerMil, newDeaths, newDeathsPerMil]
    return countryInfo
    
#This is a test for our function    


print(scrape_country('USA','https://www.worldometers.info/coronavirus/#countries'))