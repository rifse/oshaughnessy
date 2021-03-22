#!/home/user/environments/oshaughnessy/bin/python3.8

import itertools
import json
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


class Rate:

    def __init__(self, refresh=False):

        try:
            if refresh:
                with open('symbols.json', 'r') as dataFile:
                    data_symbols = json.load(dataFile)
                    symbols = data_symbols['symbols']
                for symbol in symbols:
                    # request new data w/ Data.get_symbol()
                    pass
            else:
                with open('data_finviz.csv', 'r') as dataFile:
                    self.data = pd.read_csv(dataFile, index_col=0)
        except FileNotFoundError:
            # maybe have to __init__ Data and will take >48h:
            # call Data.make_symbols 
            pass

    def main(self):
        relevant = ['P/B', 'P/E', 'P/S']  # + P/C or P/FCF?
        self.data = self.data[relevant]
        for x in relevant:
            self.data[f'{x}_r'] = self.data[x].rank(ascending=False, pct=True)
        dropped = self.data.drop(labels=relevant, axis=1)
        self.data['rate'] = dropped.sum(axis=1)
        self.data.sort_values('rate', inplace=True)
        print(self.data['rate'].to_string())

if __name__ == '__main__':
    rate = Rate()
    rate.main()
