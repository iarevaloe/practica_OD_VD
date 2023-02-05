import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
import time
import csv
import itertools
import sys

def data_weather_daily(html):
    weather_table_columns = [
        'day', 
        'temperature_max', 
        'temperature_avg', 
        'temperature_min', 
        'dew_point_max', 
        'dew_point_avg', 
        'dew_point_min', 
        'humidity_max', 
        'humidity_avg', 
        'humidity_min',
        'wind_speed_max',
        'wind_speed_avg',
        'wind_speed_min',
        'preasure_max',
        'preasure_avg',
        'preasure_min',
        'precipitation']
    
    expansion_web = BeautifulSoup(html, 'html.parser')

    table_weather = expansion_web.find('table', {'class':'days ng-star-inserted'})
    table_body = table_weather.find('tbody')

    subtables_table_weather = table_body.find_all('table')

    dataframe_weather_month = pd.DataFrame()
    
    for table in subtables_table_weather:
        table_df = (pd.read_html(str(table), header = 0, encoding = 'utf-8', decimal = '.', thousands = ',')[0])
        dataframe_weather_month = pd.concat([dataframe_weather_month, table_df], axis=1)

    dataframe_weather_month.columns = weather_table_columns

    return(dataframe_weather_month)

def get_weather_daily_city_years(city, state, abbreviation_state, year_init, year_final):

    url = 'https://www.wunderground.com'

    browser = webdriver.Chrome('driver\chromedriver.exe')
    browser.get(url)
    
    WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button#truste-consent-button')))
    cookies_button = browser.find_element(By.CSS_SELECTOR, 'button#truste-consent-button')
    cookies_button.click()
    WebDriverWait(browser, 20).until(EC.invisibility_of_element_located((By.ID, 'truste-consent-content')))
    
    search_text = browser.find_element(By.CSS_SELECTOR, 'input#wuSearch')
    search_text.click()
    search_text.clear()
    state_capital_abbreviation = city + ', ' + state
    search_text.send_keys(state_capital_abbreviation)
    time.sleep(4)
    search_text.send_keys(Keys.ENTER)

    WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'ul li.ng-star-inserted:nth-child(5) a.ng-star-inserted')))
    history = browser.find_element(By.CSS_SELECTOR, 'ul li.ng-star-inserted:nth-child(5) a.ng-star-inserted')
    history.click()

    WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH,'//a[text()=\'Monthly\']')))
    monthly = browser.find_element(By.XPATH, '//a[text()=\'Monthly\']')
    monthly.click()
    
    list_weather_city = []

    for year in range(year_init, year_final):
    
        for month in range(1, 13):  
            select_year = Select(WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 
                                                                                              'select#yearSelection'))))
            select_year.select_by_visible_text(str(year))

            select_month = Select(WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 
                                                                                               'select#monthSelection'))))
            select_month.select_by_value(str(month))

            date_submit = WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 
                                                                                       'input#dateSubmit')))
            date_submit.click()
            
            try:
                WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 
                                                                                 'table.days.ng-star-inserted')))
                html = browser.page_source
            
                data_weather_city_month = data_weather_daily(html)
                data_weather_city_month = data_weather_city_month.assign(state=abbreviation_state, 
                                                                         year=year, 
                                                                         month=month)
            
                list_weather_city.append(data_weather_city_month)
                pass
            except:
                print('No se encuentran registros del ' + str(month) + '/' + str(year) \
                      + ' para la ciudad de ' + city + ' (' + state + ')')
                continue
    try:
        df_weather_city = pd.concat(list_weather_city).reset_index(drop=True)
        df_weather_city.to_csv('data\weather_' + abbreviation_state + '.csv', index = False)
    except:
        print('No se han extraído datos para la ciudad de ' + city + ' (' + state + ')')
        
    

states_capital_eeuu = pd.read_csv('data\capital_eeuu\eeuu_states_capital.csv')

for index, state in states_capital_eeuu.iterrows():
    get_weather_daily_city_years(state.capital, state.state, state.abbreviation, 2018, 2023)
    


