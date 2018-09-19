# -*- coding: UTF-8 -*-
import pandas as pd
# import pymysql
import ConfigParser
import datetime
from sqlalchemy import create_engine
from Lottery import Dlt

def dlt_con():

    conf = ConfigParser.ConfigParser()
    conf.read("db.conf")

    db_host = conf.get("db", "db_host")
    db_user = conf.get("db", "db_user")
    db_pass = conf.get("db", "db_pass")
    db_port = conf.getint("db", "db_port")
    db_name = 'lottery'

    # db = pymysql.connect(host=db_host, user=db_user, passwd=db_pass, port=db_port, db='lottery', charset='utf8')
    # return db
    engine = create_engine('mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8' % (db_user, db_pass, db_host, db_port, db_name))
    return engine


def dlt_to_date():
    # 读取数据

    engine = dlt_con()
    dlts = pd.read_sql('dlt', engine, index_col="id")

    # for k in years:
    #    for j in range(1, 156):
    #        if dlts[(dlts['year'] == k) & (dlts['term'] == j)].empty:
    #            print((k-2000)*1000+j)

    try:
        for indexes in dlts.index:
            dlt = dlts.loc[indexes]
            for i in range(10):
                col_name = 'd%d' % (i+1)
                blue = 'b%d' % (i / 5 + 1)
                red = 'r%d' % (i % 5 + 1)
                year = dlt['year']
                month = dlt[blue]
                day = dlt[red]
                date = datetime.datetime.strptime(str(dlt['date']), '%Y%m%d').date()
                # print date
                dlts.loc[indexes, 'real_date'] = date
                # print i, month, day
                tmp_date = datetime.date(year, month, 1)
                weekday = datetime.date.weekday(tmp_date)
                delta = int(day - weekday - 1)
                # print type(delta), delta
                ball_date = tmp_date + datetime.timedelta(days=delta)
                # print date
                dlts.loc[indexes, col_name] = ball_date

        #new_dlts = dlts[['term', 'ball', 'real_date', 'd1', 'd2', 'd3', 'd4', 'd5']]
        #new_dlts.to_sql('dlt_date', engine, if_exists='replace')
        # dlts.to_sql('dlt_with_date_all', engine, if_exists='replace')
        dlts.to_csv('dlt_with_date_all.csv', sep=',')

    except Exception as err:
        print err

    return


def dlt_fetch():
    dlts = pd.DataFrame(columns=('id', 'year', 'term', 'date', 'r1', 'r2', 'r3', 'r4', 'r5', 'b1', 'b2'))
    dlts.set_index('id')
    this_year = datetime.datetime.now().year

    for j in range(2000, this_year + 1):
        for i in range(1, 156):
            try:
                print i, j
                dlt = Dlt(j, i)
                if dlt.fetch_data():

                    date = datetime.datetime.strptime(dlt.date, '%Y%m%d').date()
                    # print dlt.num

                    a = [dlt.id, j, i, date]
                    a = a + dlt.num

                    dlts.loc[dlt.id] = a
                    # print dlts


            except Exception as err:
                print err
                continue

    dlts.to_csv('dlt_all.csv', sep=',')
    return


if __name__ == '__main__':
    dlt_fetch()

