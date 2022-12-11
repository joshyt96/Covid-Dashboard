import json
from math import pi
import datetime
from datetime import date


today = str(date.today())
toad = today.split('-')
today = datetime.date(int(toad[0]),int(toad[1]),int(toad[2]))
yesterday = datetime.date(int(toad[0]),int(toad[1]),int(toad[2])-1)
twodays = datetime.date(int(toad[0]),int(toad[1]),int(toad[2])-2)

f1 = open(f'{today}-table.json')
Dictionary = json.load(f1)
f1.close()
f2 = open(f'{yesterday}-table.json')
yesterdayDictionary = json.load(f2)
f2.close()
f3 = open(f'{twodays}-table.json')
twodaysDictionary = json.load(f3)
f3.close()    

Countries = list(Dictionary.keys())
Countries.remove('World')
country10 = Countries[0:10]

new_cases = []
yesterday_new_cases = []
twodays_new_cases = []
i = 0
for m in country10:
    if Dictionary[m][1] == '':
        Dictionary[m][1] = '0'
    new_cases.append(int(Dictionary[m][1].replace(',','')))
    if yesterdayDictionary[m][1] == '':
        yesterdayDictionary[m][1] = '0'
    yesterday_new_cases.append(int(yesterdayDictionary[m][1].replace(',','')))
    if twodaysDictionary[m][1] == '':
        twodaysDictionary[m][1] = '0'
    twodays_new_cases.append(int(twodaysDictionary[m][1].replace(',','')))
    m = [new_cases[i],yesterday_new_cases[i],twodays_new_cases[i]]
    print(i)
    i = i+1
    print(m)

