""" grubhubData.py

This script allows to scrape restaurant data from grubhub website based on different cities and zipcode
Data variables: restaurant name, restaurant delivery time, payment methods, customer reviews

This script requires that `pandas`, `selenium`, `selenium exceptions`, `time` be installed within the Python
environment.

This file can also be imported as a module and contains the following
functions:
    * login - function to login to grubhub website
    * calculate_rating - function to calculate rating of restaurants
    * create_dataframe - function to create dataframe
    * select_delivery option - function to select delivery / pickup
    * search_city - function to search location of restaurant
    * logout - function to logout from grubhub website
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd


def logout(driver):
    """
    logout function is used for closing selenium web driver connection

    :param driver: selenium web driver to establish the connection with Firefox
    :return: None
    """
    driver.quit()


def calculate_rating(background_position):
    """
    calculate_rating function is used for calculating restaurant's ratings

    :param background_position: position of div element in browser
    :return: rating
    """
    if background_position == "background-position: 0px -192px;":
        rating = 5
    elif background_position == "background-position: 0px -168px;":
        rating = 4.5
    elif background_position == "background-position: 0px -144px;":
        rating = 4
    elif background_position == "background-position: 0px -120px;":
        rating = 3.5
    elif background_position == "background-position: 0px -96px;":
        rating = 3
    elif background_position == "background-position: 0px -72px;":
        rating = 2.5
    elif background_position == "background-position: 0px -48px;":
        rating = 2
    elif background_position == "background-position: 0px -24px;":
        rating = 1.5
    elif background_position == "background-position: 0px 0px;":
        rating = 1
    return rating


def create_data_frame(driver):
    """
    create_data_frame is used to append each restaurant's data as a new row in a dataframe

    :param driver: selenium web driver to establish the connection with Firefox
    :return: None
    """
    zipcode = 80202
    location = 'Denver'
    columns = {'Name': [], 'Reviews': [], 'PriceRange': [], 'DeliveryTime': [], 'Cuisine': [], 'Zipcode': [],
               'Location': []}
    dataframe = pd.DataFrame(columns)
    dt = driver.find_elements_by_xpath('/html/body/ghs-site-container/span/span[2]/ghs-app-content/div[3]/div/'
                                       'ghs-router-outlet/span/span/span[1]/div/div[2]/div/div[2]/div/div/span/'
                                       'ghs-search-results/div[1]/div/div[4]/div/span/span/span/div/div[*]/span/span/'
                                       'div/div/div[2]/div[1]/div[2]/div/span/span/span/span[1]')
    d_time_list = list()
    for x in range(len(dt)):
        d_time_list.append(dt[x].text + "minutes")
    restaurant_links = driver.find_elements_by_xpath('/html/body/ghs-site-container/span/span[2]/ghs-app-content/div[3]'
                                                     '/div/ghs-router-outlet/span/span/span[1]/div/div[2]/div/div[2]/'
                                                     'div/div/span/ghs-search-results/div[1]/div/div[4]/div/span/span/'
                                                     'span/div/div[*]/span/span/div/div/div[1]/div/div/div/div/a/h5')
    for ele in range(len(restaurant_links)):
        if ele >= 1:
            restaurant_links = driver.find_elements_by_xpath('/html/body/ghs-site-container/span/span[2]/'
                                                             'ghs-app-content/div[3]/div/ghs-router-outlet/span/span/'
                                                             'span[1]/div/div[2]/div/div[2]/div/div/span/'
                                                             'ghs-search-results/div[1]/div/div[4]/div/span/span/span/'
                                                             'div/div[*]/span/span/div/div/div[1]/div/div/div/div/a/h5')
        name = restaurant_links[ele].text
        time.sleep(5)
        restaurant_links[ele].click()
        time.sleep(5)
        rating_element = driver.find_element_by_xpath('/html/body/ghs-site-container/span/span[2]/ghs-app-content/div[3]/div/ghs-router-outlet/span/ghs-restaurant-provider/span[2]/div/div[1]/div/main/span[6]/div/span[2]/div/div/div[2]/div[3]/span[1]/span/div/span/div/span[1]/div')
        background_position = rating_element.get_attribute('style')
        rating = calculate_rating(background_position)
        print(rating)
        pr = driver.find_element_by_xpath('/html/body/ghs-site-container/span/span[2]/ghs-app-content/div[3]/div/'
                                          'ghs-router-outlet/span/ghs-restaurant-provider/span[2]/div/div[1]/div/div/'
                                          'div/div/div/div[1]/span[1]/div/div[1]/span/div/div[2]')
        cs = driver.find_element_by_xpath('/html/body/ghs-site-container/span/span[2]/ghs-app-content/div[3]/div/'
                                          'ghs-router-outlet/span/ghs-restaurant-provider/span[2]/div/div[1]/div/div/'
                                          'div/div/div/div[1]/span[1]/div/div[1]/div/span[1]')
        try:
            reviews_link = driver.find_elements_by_xpath('/html/body/ghs-site-container/span/span[2]/ghs-app-content/'
                                                        'div[3]/div/ghs-router-outlet/span/ghs-restaurant-provider/'
                                                        'span[2]/div/div[1]/div/div/div/div/div/span[1]/span/div/div/'
                                                        'div/div[2]/div/div[*]/span/div/div[2]/p')
        except NoSuchElementException:
            reviews = 'Null'
            dataframe.loc[len(dataframe.index)] = [name, reviews, pr.text, dt.text, cs.text, zipcode, location]
            driver.back()
            time.sleep(5)
            continue

        for i in range(len(reviews_link)):
            dataframe.loc[len(dataframe.index)] = [name, reviews_link[i].text, pr.text, d_time_list[ele], cs.text,
                                                   zipcode, location]
        driver.back()
        time.sleep(5)
        dataframe.to_csv('80202_1.csv')
    logout(driver)


def select_delivery_option(driver):
    """
    select_delivery_location is used to select the delivery mode of a restaurant

    :param driver: selenium web driver to establish the connection with Firefox
    :return: None
    """
    delivery = driver.find_element_by_xpath('/html/body/ghs-site-container/span/span[2]/ghs-app-content/div[3]/div/'
                                            'ghs-router-outlet/span/span/span[1]/div/div[2]/div/div[1]/div/span[3]/div/'
                                            'div[2]/div/div/span/span/aside/section/div/div/div/div/span/div/div/'
                                            'button[1]/div')
    delivery.click()
    time.sleep(20)
    create_data_frame(driver)


def search_city(driver):
    """
    search_city is used to query the zipcode of a particular city

    :param driver: selenium web driver to establish the connection with Firefox
    :return: None
    """
    search = driver.find_element_by_xpath('/html/body/ghs-site-container/span/span[2]/ghs-app-content/div[3]/div/'
                                          'ghs-router-outlet/span/span/span[2]/div/div[2]/div[2]/div[2]/span/div/div[1]'
                                          '/div/span/ghs-address-input/div/div/div/input')
    search.send_keys('80202' + Keys.ENTER)
    time.sleep(10)
    select_delivery_option(driver)


def login():
    """
    login is used to provide credentials and establishing live connection

    :param driver: selenium web driver to establish the connection with Firefox
    :return: None
    """
    # driver = webdriver.Chrome(
    #     executable_path="/Users/mayank/GitHub/ICE_python/web-scraping-dynamic-webpages-ice-talrejamayank1/chromedriver")
    driver = webdriver.Firefox(executable_path=r'C:\Users\14057\Documents\WEB SCRAPING\geckodriver-v0.30.0-win64'
                                               r'\geckodriver.exe')
    url = 'https://www.grubhub.com/'
    driver.get(url)
    time.sleep(10)
    search_city(driver)


if __name__ == "__main__":
    login()
