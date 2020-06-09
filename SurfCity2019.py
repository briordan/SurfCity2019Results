from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd

import time

def test_run():
    chromeOptions = Options()
    #chromeOptions.add_argument("--incongnito")
    chromeOptions.add_argument("--headless")

    driver = webdriver.Chrome("d:/WebDriver/chromedriver", options=chromeOptions)
    driver.get("https://www.motivrunning.com/run-surf-city/results-photos/#xact_results_tabs_agegroup")

    time.sleep(12) #the results page needs time to load
    length = Select(driver.find_element_by_xpath("//select[@name='xact_results_agegroup_results_length']"))
    length.select_by_value('100') # select 100 results per page

    race = Select(driver.find_element_by_xpath("//select[@id='xact_results_agegroup_race']"))
    race.select_by_value('5806') #Select the marathon distance, the site coded it as 5806

    time.sleep(3)
    driver.find_element_by_id("xact_results_agegroup_search").click()
    time.sleep(5)
    next = driver.find_element_by_id('xact_results_agegroup_results_next') #get the next button

    page_source_overview = driver.page_source
    soup = BeautifulSoup(page_source_overview, 'lxml')

    results = soup.find_all('table', {'id' : 'xact_results_agegroup_results'})
    df_results = pd.read_html(str(results))[0]

    for result_page in range(2,15):  # there are 15 pages of results
        next.click()
        time.sleep(60)  # the website is sometimes slow to responding to the click event
        page_source_overview = driver.page_source
        soup = BeautifulSoup(page_source_overview, 'lxml')
        results = soup.find_all('table', {'id': 'xact_results_agegroup_results'})
        result_array = pd.read_html(str(results))[0]
        df_results = pd.concat([df_results, result_array], ignore_index= True)
        print("on results page: " + str(result_page))

    driver.quit()

    # Seperate Sex/Age to two columns
    for index, row in df_results.iterrows():
        df_results.at[index, 'Sex'] = df_results.at[index,'Sex/Age'][0]
        df_results.at[index, 'Age'] = df_results.at[index, 'Sex/Age'][2:]
        if (len(df_results.at[index, 'City']) > 4):
            df_results.at[index, 'State'] = df_results.at[index, 'City'][-2:]
            df_results.at[index, 'City'] = df_results.at[index,'City'][:-2]

    df_results.drop(df_results.columns[[0]], axis=1, inplace=True)  # drop column 0
    df_results.to_csv("SurfCity2019.csv", index=False)

if __name__ == "__main__":
    test_run()