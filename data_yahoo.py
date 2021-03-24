#!/home/admin/envs_py/oshaughnessy/bin/python3.8

import json
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import pandas as pd

# could contain additional info:
# https://finance.yahoo.com/quote/{symbol}/financials?p={symbol}
# https://finance.yahoo.com/quote/{symbol}/balance-sheet/?p={symbol}
# https://finance.yahoo.com/quote/{symbol}/cash-flow/?p={symbol}


class Data:

    def __init__(self):

        self.data = pd.DataFrame()
        try:
            with open('data_yahoo.csv', 'r') as dataFile:
                self.data = pd.read_csv(dataFile, index_col=0)
        except FileNotFoundError:
            # self.data = pd.DataFrame()
            try:
                with open('symbols.json', 'r') as dataFile:
                    symbols = json.load(dataFile)['symbols']
                self.data = self.get_symbols(symbols)
            except FileNotFoundError:
                print("RUN data_finviz.py FIRST, WILL TAKE >48h")

    @staticmethod
    def get_symbols(symbols, start=False, close=False):
    
        garbage = []
        options = Options()
        options.headless = True
        driver = webdriver.Firefox(options=options, executable_path='../geckodriver')
        driver.implicitly_wait(10)
        try:
            driver.get(f'https://finance.yahoo.com/quote/{symbols[0]}/key-statistics')
            driver.find_element_by_css_selector('[name=agree]').click()  # oauth
            data = pd.concat(pd.read_html(driver.page_source))
            data.set_index(data.columns[0], inplace=True)
        except Exception as e:
            garbage.append(symbols[0])
        for sym in symbols[1:]:
            try:
                driver.get(f'https://finance.yahoo.com/quote/{sym}/key-statistics')
                frames = pd.concat(pd.read_html(driver.page_source))
                frames.set_index(frames.columns[0], inplace=True)
                data = pd.concat([data, frames], axis=1)
            except Exception as e:
                garbage.append(sym)
                print(f'exception {e} for symbol {sym}')
                return None
        driver.close()   
        for sym in garbage:
            symbols.remove(sym)
        data.set_axis(symbols, axis=1, inplace=True)

        return data.T


if __name__ == '__main__':
    data = Data()
    result = data.data
    result.to_csv('data_yahoo.csv')
    # print(result)
