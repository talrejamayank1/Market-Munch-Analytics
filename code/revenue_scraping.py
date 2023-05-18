""" revenue_scraping.py

This script allows to scrape restaurants revenue data from google
Data variables: revenue

This script requires that `pandas`, `selenium`, `selenium exceptions`, `time` , `os` be installed within the Python
environment.

This file can also be imported as a module and contains the following
functions:
    * addRevenueColumn - function to add revenue column to the main dataframe
    * revenueQuery - function to scrape revenue data for all the restaurants
"""

import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import os

# Modifying pandas default max columns and max rows size
pd.options.display.max_columns = None
pd.options.display.max_rows = None
pd.options.display.width = None

# set working directory
dir = r'C:\Users\14057\Documents\SPRING 2022\DATA SCIENCE PROGRAMMING AND ANALYTICS II\PROJECT\msis-5223-deliverable-1-nsms\data'
os.chdir(dir)

# read data
data = pd.read_csv('scraped_data.csv')
revenue_data = pd.read_csv('revenue_data.csv')
restaurants = data['Name'].to_numpy()

revenue_list = []

def addRevenueColumn():
    """
    addRevenueColumn is used to add revenue column to the main dataframe
    :return: None
    """
    revenue_data = pd.read_csv('revenue_data.csv')
    revenue_column = revenue_data['Revenue'].to_numpy()
    for i in range(len(revenue_column)):
        revenue_column[i] = float(revenue_column[i])
        if revenue_column[i] == 0:
            revenue_column[i] = 8.53  # restaurants with 0 revenue are replaced with the average of all restaurants revenue
    data['Revenue'] = revenue_column
    data.to_csv(
        'C:/Users/14057/Documents/SPRING 2022/DATA SCIENCE PROGRAMMING AND ANALYTICS II/PROJECT/msis-5223-deliverable-1-nsms/data/scraped_data.csv', sep=',')


def revenueQuery():
    """
    revenueQuery is used to scrape revenue of each restaurant if available
    :return: None
    """
    columns = {'Revenue': []}
    dataframe = pd.DataFrame(columns)
    driver = webdriver.Firefox(executable_path=r'C:\Users\14057\Documents\FALL 2021\DATA SCIENCE PROGRAMMING AND ANALYTICS I\WEB SCRAPING\geckodriver-v0.30.0-win64'
                                               r'\geckodriver.exe')
    url = "https://www.google.com/"
    driver.get(url)
    #time.sleep(2)
    for i in range(len(restaurants)):
        print(i)
        searchBar = driver.find_element_by_css_selector(
            "html body div.L3eUgb div.o3j99.ikrT4e.om7nvf form div div.A8SBwf div.RNNXgb div.SDkEP div.a4bIc input.gLFyf.gsfi")
        searchBar.send_keys(restaurants[i] + " " + "revenue")
        driver.find_element_by_css_selector("html body div.L3eUgb div.o3j99.LLD4me.yr19Zb.LS8OJ").click()
        searchButton = driver.find_element_by_css_selector("html body div.L3eUgb div.o3j99.ikrT4e.om7nvf form div div.A8SBwf div.FPdoLc.lJ9FBc center input.gNO89b")
        searchButton.click()
        time.sleep(2)
        try:
            revenue = driver.find_element_by_css_selector("html body#gsr.srp div#main.main div#cnt.e9EfHf div#rcnt.GyAeWb div#center_col.s6JM6d div#res.eqAnXb div#search div div#rso.v7W49e div.ULSxyf block-component div.g.mnr-c.JnwWd.g-blk div.dG2XIf.EyBRub.XzTjhb div.L29P6c.fm06If div div.xpdopen div.ifM9O div div div.kp-header div.TrpAt.kp-rgc div.DI6Ufb div.EfDVh.wDYxhc.NFQFxe.viOShc.LKPcQc div.HwtpBd.gsrt.PZPZlf.kTOYnf div.Z0LcW")
            revenue_list.append(revenue.text)
            dataframe.loc[len(dataframe.index)] = [revenue.text]
            dataframe.to_csv('C:/Users/14057/Documents/SPRING 2022/DATA SCIENCE PROGRAMMING AND ANALYTICS II/PROJECT/msis-5223-deliverable-1-nsms/data/revenue_data.csv', sep=',')
        except NoSuchElementException:
            revenue_list.append(0)
            dataframe.loc[len(dataframe.index)] = [0]
            dataframe.to_csv(
                'C:/Users/14057/Documents/SPRING 2022/DATA SCIENCE PROGRAMMING AND ANALYTICS II/PROJECT/msis-5223-deliverable-1-nsms/data/revenue_data.csv',
                sep=',')
        driver.back()
        time.sleep(2)
    addRevenueColumn()


if __name__ == "__main__":
    revenueQuery()
