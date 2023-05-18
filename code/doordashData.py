""" doordashData.py

This script allows to scrape restaurant data from doordash website based on different cities and zipcode
Data variables: restaurant name, restaurant rating, restaurant delivery fees, restaurant delivery time, payment methods,
customer reviews

This script requires that `pandas`, `selenium`, `selenium exceptions`, `time` be installed within the Python
environment.

This file can also be imported as a module and contains the following
functions:
    * login - function to login to doordash website
    * create_dataframe - function to create dataframe
    * get_restaurant_list - function to get lists of restaurants from doordash based on cities and pin code
    * logout - function to logout from doordash website * login - function to login to doordash website
    * create_dataframe - function to create dataframe
    * logout - function to logout from doordash website
"""
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time


# Modifying pandas default max columns and max rows size
pd.options.display.max_columns = None
pd.options.display.max_rows = None
pd.options.display.width = None


def logout(driver):
    """
    logout function is used for closing selenium web driver connection

    :param driver: selenium web driver to establish the connection with Firefox
    :return: None
    """
    driver.quit()


def create_dataframe(driver):
    """
    create_dataframe is used to append each restaurant's data as a new row in a dataframe

    :param driver: selenium web driver to establish the connection with Firefox
    :return: None
    """
    columns = {'Name': [], 'Rating': [], 'Reviews': [], 'Price Range': [], 'Delivery Fees': [], 'Delivery Time': [],
               'Cuisine': [], 'PinCode': [], 'Location': [], 'Payment Methods': [], 'Distance': [], 'Source': []}
    dataframe = pd.DataFrame(columns)
    restaurants = driver.find_elements_by_css_selector('[data-anchor-id="StoreLayoutListContainer"]>div>a')
    print(len(restaurants))
    pinCode = 29209
    location = 'Columbia'
    payment_methods = 'Paypal, Credit/Debit Card'
    source = 'Doordash'
    for x in range(len(restaurants)):
        name = driver.find_element_by_css_selector(f'[data-anchor-id="StoreLayoutListContainer"]>div:nth-child({x + 1})'
                                                   f'>div>div:nth-child(2)>a>div>div:nth-child(2)>span')
        current_name = name.text
        print(current_name)
        if current_name == '7-Eleven' \
                or current_name == 'CVS' \
                or current_name == 'DashMart' \
                or current_name == 'Bartell Drugs' or current_name == 'The PotLuck':
            continue
        try:
            delivery_fees_selector = driver.find_element_by_css_selector(f'[data-anchor-id="StoreLayoutListContainer"]'
                                                                         f'>div:nth-child({x + 1})>div>div:nth-child(2)>a>div'
                                                                         f'>div:nth-child(4)>div:nth-child(2)>span')
            delivery_fees = delivery_fees_selector.text
        except NoSuchElementException:
            delivery_fees = 0
        try:
            delivery_time_selector = driver.find_element_by_css_selector(f'[data-anchor-id="StoreLayoutListContainer"]'
                                                                         f'>div:nth-child({x + 1})>div>div:nth-child(2)>a>div'
                                                                         f'>div:nth-child(3)>div:nth-child(2)>div>span')
            delivery_time = delivery_time_selector.text
        except NoSuchElementException:
            delivery_time = 0
        try:
            cuisine_selector = driver.find_element_by_css_selector(f'[data-anchor-id="StoreLayoutListContainer"]'
                                                                   f'>div:nth-child({x + 1})>div>div:nth-child(2)>a>div'
                                                                   f'>div:nth-child(3)>div:nth-child(1)>span')
            cuisine = cuisine_selector.text
        except NoSuchElementException:
            cuisine = 'Null'
        try:
            rating = driver.find_element_by_css_selector(
                f'[data-anchor-id="StoreLayoutListContainer"]>div:nth-child({x + 1})'
                f'>div>div:nth-child(2)>a>div>div:nth-child(4)>div>div>div>span')
            current_rating = rating.text
        except NoSuchElementException:
            current_rating = 'Null'
        restaurant = driver.find_element_by_css_selector(
            f'[data-anchor-id="StoreLayoutListContainer"]>div:nth-child({x + 1})'
            f'>a')
        restaurant.click()
        time.sleep(5)
        try:
            distance_selector = driver.find_element_by_xpath(
                '/html/body/div[1]/div[2]/div[1]/div[1]/div[1]/header/div[2]/div[1]/div[3]/span[1]')
            distance = distance_selector.text
        except NoSuchElementException:
            distance = 'Null'
        try:
            price_range_selector = driver.find_element_by_css_selector('header>div:nth-child(2)>div>div:nth-child(3)'
                                                                       '>span:nth-child(4)')
            price_range = price_range_selector.text
        except NoSuchElementException:
            price_range = 'Null'
        try:
            see_all_reviews_button = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div/div/div[1]/div[1]/div[1]/div/button/div/div/div[1]/span')
        except NoSuchElementException:
            review = 'Null'
            dataframe.loc[len(dataframe.index)] = [current_name, current_rating, review, price_range, delivery_fees,
                                                   delivery_time, cuisine, pinCode, location, payment_methods, distance, source]
            dataframe.to_csv('C:/Users/14057/Documents/PYTHON/Online Food Industry/Columbia.csv', sep=',')
            driver.back()
            time.sleep(5)
            continue
        see_all_reviews_button.click()
        time.sleep(5)
        all_reviews_list = driver.find_elements_by_css_selector('div#root>div>div>div:nth-child(2)>div>div'
                                                                '>div:nth-child(2)>div:nth-child(2)>div.sc-htpNat')
        for z in range(len(all_reviews_list)):
            content = driver.find_element_by_css_selector(f'div#root>div>div>div:nth-child(2)>div>div>div:nth-child(2)'
                                                          f'>div:nth-child(2)>div:nth-child({z + 1})>div>div'
                                                          f'>span:nth-child(3)')
            dataframe.loc[len(dataframe.index)] = [current_name, current_rating, content.text, price_range,
                                                   delivery_fees,
                                                   delivery_time, cuisine, pinCode, location, payment_methods, distance, source]
            dataframe.to_csv('C:/Users/14057/Documents/PYTHON/Online Food Industry/Columbia.csv', sep=',')
        driver.back()
        time.sleep(5)
        driver.back()
        time.sleep(5)
    print(dataframe)
    dataframe.to_csv('C:/Users/14057/Documents/PYTHON/Online Food Industry/Columbia.csv', sep=',')
    logout(driver)


def login():
    """
    login is used to provide credentials and establishing live connection

    :param driver: selenium web driver to establish the connection with Firefox
    :return: None
    """
    driver = webdriver.Firefox(executable_path=r'C:\Users\14057\Documents\WEB SCRAPING\geckodriver-v0.30.0-win64'
                                               r'\geckodriver.exe')
    url = 'https://identity.doordash.com/auth?client_id=1666519390426295040&intl=en-US&layout=consumer_web&prompt=' \
          'none&redirect_uri=https%3A%2F%2Fwww.doordash.com%2Fpost-login%2F&response_type=code&scope=%2A&state=%2F' \
          'home%2F%7C%7Cc2d43e5d-5542-4bef-b8bb-001c8c13fd39'
    driver.get(url)
    time.sleep(5)
    user_name = driver.find_element_by_id('FieldWrapper-2')
    password = driver.find_element_by_id('FieldWrapper-3')
    login_button = driver.find_element_by_id('login-submit-button')
    user_name.send_keys('talreja.mayank02@gmail.com')
    password.send_keys('Maya#2019lat')
    login_button.click()
    time.sleep(5)
    time.sleep(10)
    create_dataframe(driver)


if __name__ == "__main__":
    login()
