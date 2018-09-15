# -*- coding: UTF-8 -*-

from Lottery import Lottery
import pymysql
import time
import ConfigParser
import datetime


def dltinsert():
    conf = ConfigParser.ConfigParser()
    conf.read("db.conf")

    db_host = conf.get("db", "db_host")
    db_user = conf.get("db", "db_user")
    db_pass = conf.get("db", "db_pass")
    db_port = conf.getint("db", "db_port")

    db = pymysql.connect(host=db_host, user=db_user, passwd=db_pass, port=db_port, db='lottery', charset='utf8')
    cursor = db.cursor()
    cursor_select = db.cursor(cursor=pymysql.cursors.DictCursor)
    sql_maxid = "SELECT year,term FROM dlt  ORDER BY id DESC LIMIT 1"
    cursor_select.execute(sql_maxid)
    maxid = cursor_select.fetchone()
    maxterm = maxid['term']
    maxyear = maxid['year']
    thisyear = datetime.datetime.now().year

    for j in range(thisyear, maxyear-1, -1):
        if thisyear > j:
            thisterm = 1
        else:
            thisterm = maxterm + 1
        for i in range(thisterm, 156):
            try:
                sql_select = "SELECT * FROM dlt  WHERE year = '%d' and term = '%d'" % (j, i)
                cursor_select.execute(sql_select)
                if cursor_select.rowcount > 0:
                    continue
                a = Lottery(4, j, i)
                if a.fetchdata(1):
                    # print a.num
                    # print a.ball
                    # print a.id
                    # print a.date
                    sql_insert = "INSERT INTO dlt(id,year,term,r1,r2,r3,r4,r5,b1,b2,ball,date) " \
                                 "VALUES ('%d', '%d', '%d', '%d', '%d', '%d', '%d', '%d', '%d', '%d', '%d', '%s')" \
                                 % (
                                 a.id, a.year, a.term, a.num['r1'], a.num['r2'], a.num['r3'], a.num['r4'], a.num['r5'],
                                 a.num['b1'], a.num['b2'], a.ball, str(a.date))
                    print sql_insert
                    cursor.execute(sql_insert)
                    db.commit()
            except Exception as err:
                print err
                continue
    cursor.close()
    cursor_select.close()
    db.close()
    return


def dltnew(lottery_type, year, term, fetch_type):
    a = Lottery(lottery_type, year, term)
    while not a.fetchdata(fetch_type):
        time.sleep(60)
        print time.localtime()
    print a.num
    return


if __name__ == '__main__':
     # dltnew(4,2018,100,1)
     dltinsert()
