# -*- coding: UTF-8 -*-

from Lottery import Lottery
import pymysql
import time
import ConfigParser


def dltinsert():
    conf = ConfigParser.ConfigParser()
    conf.read("db.conf")

    db_host = conf.get("db", "db_host")
    db_user = conf.get("db", "db_user")
    db_pass = conf.get("db", "db_pass")
    db_port = conf.getint("db", "db_port")

    db = pymysql.connect(host=db_host, user=db_user, passwd=db_pass, port=db_port, db='lottery', charset='utf8')
    cursor = db.cursor()
    for j in range(2018, 2001, -1):
        for i in range(1, 155):
            try:
                a = Lottery(4, j, i)
                if a.FetchData(2):
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
    db.close()
    return


def dltnew(tp, year, term):
    a = Lottery(tp, year, term)
    while not a.FetchData(2):
        time.sleep(60)
        print time.localtime()
    print a.num
    return


if __name__ == '__main__':
     dltnew(4,2012,119)
    # dltinsert()
