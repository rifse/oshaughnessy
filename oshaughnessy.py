#!/home/user/environments/oshaughnessy/bin/python3.8

from json import load
import pandas as pd
from numpy import nan

pd.options.mode.use_inf_as_na = True
pd.set_option('display.max_colwidth', 10)


class Rate:

    def __init__(self):

        self.sources = ['finviz', 'yahoo']  # order of elements IS important here
        self.relevant = ['P/B', 'P/E', 'P/S', 'Enterprise Value/EBITDA 6']  # + P/C or P/FCF or ..?
        self.data = pd.DataFrame()
        try: 
            with open('DATA.csv', 'r') as dataFile:
                self.data = pd.read_csv(dataFile, index_col=0)
        except FileNotFoundError:
            self.get_data()
            self.data.to_csv('DATA.csv')


    def main(self):

        for x in self.relevant:
            self.data[f'{x}_r'] = self.data[x].rank(pct=True)
        relevant_r = self.data.drop(labels=self.relevant, axis=1)
        self.data['rate'] = relevant_r.sum(axis=1)
        self.data.sort_values('rate', inplace=True)
        self.data.to_csv('RESULT.csv')


    def get_data(self):

        temp = {}
        for name in self.sources:
            try:
                with open(f'data_{name}.csv', 'r') as dataFile:
                    temp[name] = pd.read_csv(dataFile, index_col=0)
            except FileNotFoundError as e:
                print(f'{e.args} NOT FOUND')
        if 'finviz' not in temp:
            from data_finviz import Data as Finviz
            temp['finviz'] = Finviz().data
        if 'yahoo' not in temp:
            from data_yahoo import Data as Yahoo
            temp['yahoo'] = Yahoo().data
            # ?
        data = temp['yahoo'].combine_first(temp['finviz'])  # this prefers data from yahoo (and sorts alphabethically)
        data = data.iloc[1:]  # drop first row
        data = data.replace(['-', ''], nan)  #  [ |-] -> NaN
        data.fillna(data.median(), inplace=True)  # NaN -> median
        self.data = data[self.relevant]


if __name__ == '__main__':
    rate = Rate()
    rate.main()
