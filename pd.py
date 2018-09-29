# -*- coding: UTF-8 -*-
import pandas as pd
# import pymysql
import ConfigParser
import datetime
import calendar
from sqlalchemy import create_engine
from Lottery import Dlt


def dlt_con():  # 数据库链接

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


def dlt_from_sql_to_date():  # 从数据库读取数据

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
                dlts.loc[indexes, col_name] = ball_to_date(year, int(day), int(month))
                dlts.loc[indexes, 'real_date'] = date

        #new_dlts = dlts[['term', 'ball', 'real_date', 'd1', 'd2', 'd3', 'd4', 'd5']]
        #new_dlts.to_sql('dlt_date', engine, if_exists='replace')
        # dlts.to_sql('dlt_with_date_all', engine, if_exists='replace')
        dlts.to_csv('dlt_from_sql_to_date.csv', sep=',')

    except Exception as err:
        print err

    return


def dlt_from_csv_to_date(fetch_type):

    dlts = pd.read_csv('dlt_all_fetch_type_%d.csv' % fetch_type, sep=',')

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
                dlts.loc[indexes, col_name] = ball_to_date(year, int(day), int(month))

        dlts.to_csv('dlt_from_csv_to_date.csv', sep=',')

    except Exception as err:
        print err

    return


def dlt_fetch(fetch_type):
    dlts = pd.DataFrame(columns=('id', 'year', 'term', 'date', 'r1', 'r2', 'r3', 'r4', 'r5', 'b1', 'b2'))
    dlts.set_index('id')
    this_year = datetime.datetime.now().year

    for j in range(2000, this_year + 1):
        for i in range(1, 156):
            try:
                print i, j
                dlt = Dlt(j, i)
                if dlt.fetch_data(fetch_type):

                    date = datetime.datetime.strptime(dlt.date, '%Y%m%d').date()
                    # print dlt.num

                    a = [dlt.id, j, i, date]
                    a = a + dlt.num

                    dlts.loc[dlt.id] = a
                    # print dlts


            except Exception as err:
                print err
                continue

    dlts.to_csv('dlt_all_fetch_type_%d.csv' % fetch_type, sep=',')
    return


def dlt_read(csv):

    dlts = pd.read_csv(csv,sep=',')

    return dlts


def dlt_analysis(date, ball, csv):

    dlts = dlt_read(csv)

    if date.weekday() == 0:
        date_begin = date - datetime.timedelta(days=2)
        date_end = date + - datetime.timedelta(days=2)
    elif date.weekday() == 2:
        date_begin = date - datetime.timedelta(days=2)
        date_end = date + datetime.timedelta(days=3)
    elif date.weekday() == 5:
        date_begin = date - datetime.timedelta(days=3)
        date_end = date + datetime.timedelta(days=2)
    else:
        print 'date err!!', date.weekday()
        return False

    print dlts.loc[dlts['real_date'] == date.strftime('%Y-%m-%d'), ['id', 'ball', 'real_date', 'r1', 'r2',
                                                                    'r3', 'r4', 'r5', 'b1', 'b2']]

    # print date_begin, date_end, date, date.weekday()

    dates = []
    balls = []

    for indexes in dlts.index:
        dlt = dlts.loc[indexes]
        real_date = datetime.datetime.strptime(dlt['real_date'], '%Y-%m-%d')
        analy_date_begin = real_date.replace(month=date_begin.month, day=date_begin.day)
        analy_date_end = real_date.replace(month=date_end.month, day=date_end.day)
        #print analy_date

        for i in range(10):
            col_name = 'd%d' % (i + 1)
            # print pd.to_datetime(dlt[col_name]), analy_date
            # print type(pd.to_datetime(dlt[col_name])) , type(analy_date)
            # print pd.to_datetime(dlt[col_name]) - analy_date
            if (analy_date_begin < pd.to_datetime(dlt[col_name]) < analy_date_end) \
                    and (dlt['ball'] == ball or dlt['ball'] == 0):
                # print date, col_name, dlt[col_name], real_date, ball
                dates.append((real_date.year, real_date.month, real_date.day))

    dates = list(set(dates))

    for date in dates:
        theball = date_to_ball(date[0], date[1], date[2])
        # print(date, theball)
        for ball in theball:
            balls.append(tuple(ball))
    balls = list(set(balls))
    balls.sort()

    print balls

    return


def ball_to_date(year, red, blue):

    tmp_date = datetime.date(year, blue, 1)
    weekday = datetime.date.weekday(tmp_date) + 1
    turn_weekday = weekday % 7
    delta = red - turn_weekday - 1
    # print type(delta), delta
    ball_date = tmp_date + datetime.timedelta(days=delta)

    return ball_date


def date_to_ball(year, month, day):

    nums = []
    date = datetime.date(year, month, day)

    # case 1
    tmp_date1 = datetime.date(year, month, 1)
    weekday1 = datetime.date.weekday(tmp_date1) + 1
    red1 = day + weekday1 % 7
    blue1 = month

    date1 = ball_to_date(year, red1, blue1)
    if (0 < red1 < 36) and (date1 == date):
        nums.append([red1, blue1])

    # case 2
    tmp_date2 = datetime.date(year, month, day)
    weekday2 = datetime.date.weekday(tmp_date2) + 1
    red2 = weekday2 % 7 + 1
    if month == 12:
        year2 = year + 1
        blue2 = 1
    else:
        year2 = year
        blue2 = month + 1

    date2 = ball_to_date(year2, red2, blue2)
    if (0 < red2 < 36) and (date2 == date):
        nums.append([red2, blue2])

    # case3
    tmp_date3 = tmp_date1 - datetime.timedelta(days=1)
    weekday3 = datetime.date.weekday(tmp_date3) + 1
    red3 = 29 + weekday3 % 7 + day
    if month == 1:
        year3 = year - 1
        blue3 = 12
    else:
        year3 = year
        blue3 = month - 1

    date3 = ball_to_date(year3, red3, blue3)
    if (0 < red3 < 36) and (date3 == date):
        nums.append([red3, blue3])

    return nums


if __name__ == '__main__':

    csv = 'dlt_from_sql_to_date.csv'

    # dlts = dlt_read(csv)
    #
    # for indexes in dlts.loc[(dlts['id'] > 18050)].index:
    #     dlt = dlts.loc[indexes]
    #     # print dlt
    #     # print datetime.datetime.strptime(dlt['real_date'], '%Y-%m-%d').date()
    #     dlt_analysis(datetime.datetime.strptime(dlt['real_date'], '%Y-%m-%d').date(), dlt['ball'], csv)

    dlt_analysis(datetime.date(2018, 5, 7), 1, csv)
    # for k in range(2017, 2020):
    #     for j in range(1, 13):
    #         for i in range(1, 36):
    #             date = ball_to_date(k, i, j)
    #             ball = date_to_ball(date.year, date.month, date.day)
    #             print i, j, date, ball

    # for date in list(datetime.date(2017, 1, 1) + datetime.timedelta(days=x) for x in range(0, 800)):
    #     for num in date_to_ball(date.year, date.month, date.day):
    #         print date, num, ball_to_date(date.year, num[0], num[1])

     # nums = date_to_ball(2018, 11, 3)
     # date = ball_to_date(2018, 35, 10)

     # print nums
     # print date

    # dlt_from_sql_to_date()

