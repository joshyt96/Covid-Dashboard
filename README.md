# Covid-Dashboard
COVID Dashboard
by: Trevor, Elle, Josh

This program scrapes data from https://www.worldometers.info/coronavirus/ and displays it in a GUI for easy reading and interpretation. 

## Part One
For this part of the assignment, we were ask to commit code that successfully scrapes COVID death data from the web. We have also made a function, scrape_country, that asks accepts a URL and country name which outputs a list with death data for the chosen country. Example of how to use the function:

First parameter is the URL. Note, this function only works with 'https://www.worldometers.info/coronavirus/#countries', any other URL will not work.
Second parameter is the name of the country. Note, the name you input needs to follow the same spelling that is included on the previously mentioned website. An example of this is South Korea. The table on the website lists South Korea as 'S. Korea', using anything else will not return anything from the function.

scrape_country('https://www.worldometers.info/coronavirus/#countries', 'USA')

The output of this function is a list of floats that follow this form:

[cumulative deaths, cumulative deaths per million, new deaths today, new deaths today per million]

This function also saves a .json that includes all the Country COVID data retreived from the Worldometer website. It follows a format that when used with other code will give the user a dictionary that uses country names as the key.