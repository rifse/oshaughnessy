#!/home/user/environments/oshaughnessy/bin/python3.8

# Get data as described in:
# https://medium.datadriveninvestor.com/scraping-live-stock-fundamental-ratios-news-and-more-with-python-a716329e0493

import itertools
import json
from pprint import pprint
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


class Data:

    # class for scraping off finviz
    # running make_symbols takes >48h, if interrupted NO data will persist

    def __init__(self, refresh=False):
        
        self.data = pd.DataFrame()
        try:
            with open('data_finviz.csv', 'r') as dataFile:
                self.data = pd.read_csv(dataFile, index_col=0)
        except FileNotFoundError:
            self.make_symbols(maxLen=1, save=True)  # will also populate self.data

    def make_symbols(self, maxLen=1, save=True):

        alphanum = 'abcdefghijklmnopqrstuvwxyz'  # 0123456789'
        symbols = []
        for r in range(1, maxLen+1):
            # for combo in itertools.combinations_with_replacement(alphanum, r):
            for combo in itertools.product(alphanum, repeat=r):
                c = ''.join(combo)
                html = self.get_symbol(c)
                if html:
                    symbols.append(c)
                    fundamentals = self.get_fundamentals(html)
                    self.data[c] = fundamentals['Values']
                    print(self.data[c].to_string())
        # print(self.data.to_string())
        self.data = self.data.T  # transpose
        if save:
            self.data.to_csv('data_finviz.csv')
            with open('symbols.json', 'w+') as dataFile:
                json.dump({"symbols": symbols}, dataFile)

    @staticmethod
    def get_symbol(symbol):
        url = ("http://finviz.com/quote.ashx?t=" + symbol.lower())
        try:
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            webpage = urlopen(req).read()
        except (URLError, HTTPError) as e:  # (ConnectionError, HTTPError, Timeout):
            print(f'symbol {symbol} failed because {e.reason}')
            return None
        else:
            html = soup(webpage, "html.parser")  # # link for more details)
            return html
        
    @staticmethod
    def get_fundamentals(html):
        try:
            # Find fundamentals table
            fundamentals = pd.read_html(str(html), attrs = {'class': 'snapshot-table2'})[0]
            
            # Clean up fundamentals dataframe
            fundamentals.columns = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']
            colOne = []
            colLength = len(fundamentals)
            for k in np.arange(0, colLength, 2):
                colOne.append(fundamentals[f'{k}'])
            attrs = pd.concat(colOne, ignore_index=True)
        
            colTwo = []
            colLength = len(fundamentals)
            for k in np.arange(1, colLength, 2):
                colTwo.append(fundamentals[f'{k}'])
            vals = pd.concat(colTwo, ignore_index=True)
            
            fundamentals = pd.DataFrame()
            fundamentals['Attributes'] = attrs
            fundamentals['Values'] = vals
            fundamentals = fundamentals.set_index('Attributes')
            return fundamentals

        except Exception as e:
            return None

    @staticmethod
    def get_news(html):
        try:
            # Find news table
            news = pd.read_html(str(html), attrs = {'class': 'fullview-news-outer'})[0]
            links = []
            for a in html.find_all('a', class_="tab-link-news"):
                links.append(a['href'])
            
            # Clean up news dataframe
            news.columns = ['Date', 'News Headline']
            news['Article Link'] = links
            news = news.set_index('Date')
            return news

        except Exception as e:
            return e

    @staticmethod
    def get_insider(html):
        try:
            # Find insider table
            insider = pd.read_html(str(html), attrs = {'class': 'body-table'})[0]
            
            # Clean up insider dataframe
            insider = insider.iloc[1:]
            insider.columns = ['Trader', 'Relationship', 'Date', 'Transaction', 'Cost', '# Shares', 'Value ($)', '# Shares Total', 'SEC Form 4']
            insider = insider[['Date', 'Trader', 'Relationship', 'Transaction', 'Cost', '# Shares', 'Value ($)', '# Shares Total', 'SEC Form 4']]
            insider = insider.set_index('Date')
            return insider

        except Exception as e:
            return e


if __name__ == '__main__':
    pass
    # data = Data()

    # print('fundamentals:')
    # with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    #     print(data.data)

    # print('news:')
    # print(get_news())
    # print('insider:')
    # print(get_insider())
    # print('""""""""""""""""""""""""""""""""""""""""""""')
