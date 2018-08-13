import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os
from typing import List, Callable



def get_chrome_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")
    path = os.getcwd() + "/chromedriver"
    return webdriver.Chrome(chrome_options=chrome_options, executable_path=path)

def parse_stock_file(path):
    stock_file = open(path, "r")
    stock_arr = []
    for line in stock_file:
        row_arr = line.strip().split(',')
        stock_arr.append(row_arr)
    return stock_arr

def get_main_url(ticker):
    return "https://finance.yahoo.com/quote/{0}?p={0}".format(ticker)

def get_side_url(ticker):
    return "https://finance.yahoo.com/quote/{0}/key-statistics?p={0}".format(ticker)

def create_document(all_names):
    with open('info.csv', 'w') as csvfile:
        statwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        statwriter.writerow(all_names)

def update_document(added_row):

    filename = 'tests.csv'

    with open('info.csv', 'a') as f:
        # reader = csv.reader(csvfile, delimiter=',',
        #                     quotechar='|')
        writer = csv.writer(f, delimiter=',',
                            quotechar='|')
        writer.writerow(added_row)


def get_stat_value(driver, stat_name):
    #TODO: error handling
    label = driver.find_element_by_xpath("//*[contains(text(), '{0}')]".format(stat_name))
    grandparent = label.find_element_by_xpath('../..')
    value_text = grandparent.find_elements_by_tag_name('td')[1].text
    return value_text

def main():
    stock_file_path = 'stocks.csv'
    stat_names = [
        'Market Cap',
        'Beta',
        'EPS (TTM)',
        'PE Ratio (TTM)',
    ]
    side_names = [
    'Price/Sales'
    ]
    all_names = ['Ticker'] + stat_names + side_names



    create_document(all_names)


    stock_file = parse_stock_file(stock_file_path)
    driver = get_chrome_driver()
    for stock_row in stock_file:
        ticker = stock_row[0]
        main_url = get_main_url(ticker)
        side_url = get_side_url(ticker)
        driver.get(main_url)

        added_row = [ticker]
        print(ticker)


        for stat_name in stat_names:
            stat_value = get_stat_value(driver, stat_name)

            added_row.append(stat_value)

            print("{0}: {1}".format(stat_name, stat_value))




        driver.get(side_url)
        for side_name in side_names:
            side_value = get_stat_value(driver, side_name)
            added_row.append(side_value)
            print("{0}: {1}".format(side_name, side_value))
        update_document(added_row)



main()
