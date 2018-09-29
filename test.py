# -*- coding: UTF-8 -*-

import pd
import datetime

def main():

    name = 'dlt_with_date_from_csv.csv'

    dlts = pd.dlt_read(name)

    dates = []

    for index in dlts.index:
        dlt = dlts.loc[index]
        for i in range(10):
            dates.append(dlt.iloc[i+13].encode('utf-8'))

    dates = list(set(dates))

    f = open('hello.txt', 'w')

    for date in dates:
        f.writelines(date+'\n')

    f.close()


if __name__ == '__main__':

    dates = ['2018/1/11',
            '2018/2/6',
            '2018/2/12',
            '2018/3/14',
            '2018/5/8',
            '2018/6/11',
            '2018/6/13',
            '2018/6/21',
            '2018/8/20',
            '2018/9/6',
            '2018/9/11',
            '2018/9/12',
            '2018/9/17',
            '2018/9/22',
            '2018/12/10',
            '2018/12/22',
            '2018/12/31']
    for date in dates:
        date = datetime.datetime.strptime(date, '%Y/%m/%d')
        print date , pd.date_to_ball(date.year, date.month, date.day)

