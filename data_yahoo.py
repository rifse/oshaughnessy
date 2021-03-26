#!/home/user/environments/oshaughnessy/bin/python3.8

from json import load
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
            try:
                with open('symbols.json', 'r') as dataFile:
                    symbols = load(dataFile)['symbols']
                self.data = self.get_symbols(symbols, save=True)
            except FileNotFoundError:
                print("RUN data_finviz.py FIRST, WILL TAKE >48h")

    @staticmethod
    def get_symbols(symbols, save=True):
    
        garbage = []
        click = True
        options = Options()
        options.headless = True
        data = pd.DataFrame()

        for sym in symbols:  
            if click:
                driver = webdriver.Firefox(executable_path='../geckodriver', options=options)
                driver.implicitly_wait(10)
                try:
                    driver.get(f'https://finance.yahoo.com/quote/{sym}/key-statistics')
                    driver.find_element_by_css_selector('[name=agree]').click()  # oauth
                    if data.empty:
                        data = pd.concat(pd.read_html(driver.page_source))
                        data.set_index(data.columns[0], inplace=True)
                    else:
                        frames = pd.concat(pd.read_html(driver.page_source))
                        frames.set_index(frames.columns[0], inplace=True)
                        data = pd.concat([data, frames], axis=1)
                    click = False
                    print(f'success for symbol {sym}')
                except Exception as e:
                    garbage.append(sym)
            else:
                try:
                    driver.get(f'https://finance.yahoo.com/quote/{sym}/key-statistics')
                    frames = pd.concat(pd.read_html(driver.page_source))
                    frames.set_index(frames.columns[0], inplace=True)
                    data = pd.concat([data, frames], axis=1)
                    print(f'success for symbol {sym}')
                except Exception as e:
                    garbage.append(sym)
                    driver.close()   
                    click = True
                    print(f'exception {str(e)} for symbol {sym}')
        driver.close()   
        for sym in garbage:
            symbols.remove(sym)
        data.set_axis(symbols, axis=1, inplace=True)
        data = data.T
        if save:
            data.to_csv('data_yahoo.csv')

        return data


if __name__ == '__main__':
    data = Data()
