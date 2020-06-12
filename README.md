# Surf City Marathon 2019 Results Webscraper

SurfCity2019.py is a script i wrote to scrape marathon race results and participant data from the web.

## Motivation
To use Selenium to navigate the website and BeautifulSoup to parse the results table and 
save to a dataframe for use in creating a Tableau visualization to display the race data.

The Tableau visualization using this data is at:
 https://public.tableau.com/profile/btriordan#!/vizhome/SurfCityMarathon2019/SurfCity2019

![Image of Visualization](https://github.com/briordan/SurfCity2019Results/blob/master/SurfCity.jpg)

## Usage
Running the script will save the results to SurfCity2019.csv.  The marathon website will sometimes 
take a long time to respond to clicking the next button, so it may take several runs to get 
a complete data capture. This will be addressed in an update

