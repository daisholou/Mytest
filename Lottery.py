# -*- coding: UTF-8 -*-
import urllib2
import demjson as json
import requests
from bs4 import BeautifulSoup


def request_ajax_url(url, body, referer=None, cookie=None, **headers):
    req = urllib2.Request(url)

    req.add_header('Content-Type', 'application/json')
    req.add_header('X-Requested-With', 'XMLHttpRequest')

    if cookie:
        req.add_header('Cookie', cookie)

    if referer:
        req.add_header('Referer', referer)

    if headers:
        for k in headers.keys():
            req.add_header(k, headers[k])

    postBody = json.encode(body)

    response = urllib2.urlopen(url, postBody)

    if response:
        return response


class Lottery:
    def __init__(self,lottery_type,year,term):
        self.num = {} # 球号
        self.lottery_type = lottery_type   #体彩中心彩票类型 大乐透是4
        self.year = year #年份。如2018
        self.term = term
        self.id = (year%100)*1000+term #期号
        self.num = {} # 球号
        self.numsequence = '' #读取的球号数据
        self.date = '' #日期
        self.ball = 0  #使用的是哪一套摇奖球

    def fetchdata(self,fetch_type):

        try:

            if fetch_type == 1:
                thisterm = str(self.id)
                url = "http://www.lottery.gov.cn/api/lottery_kj_detail_new.jspx?_ltype=%s&_term=%s" % (
                    self.lottery_type, thisterm)

                html = urllib2.urlopen(url)

                hjson = json.decode(html.read())

                if not hjson[0]:
                    return False

                self.numsequence = hjson[0]['lottery']['numSequence']
                self.num['r1'] = int(self.numsequence[0:2])
                self.num['r2'] = int(self.numsequence[3:5])
                self.num['r3'] = int(self.numsequence[6:8])
                self.num['r4'] = int(self.numsequence[9:11])
                self.num['r5'] = int(self.numsequence[12:14])
                self.num['b1'] = int(self.numsequence[15:17])
                self.num['b2'] = int(self.numsequence[18:20])
                self.ball = int(self.numsequence[27])
                self.date = hjson[0]['lottery']['openTime_fmt1']
            elif fetch_type == 2:
                thisterm = "%s%s"%(self.year, self.term)
                url = "https://www.scw98.com/cx/DLT.php?op=C"
                body = {'QIHao': thisterm}
                html = requests.post(url, body).content
                hsjson = json.decode(html)
                soup = BeautifulSoup(html, 'html.parser')
                all_html = soup.find_all('innerHTML')
                print hsjson, all_html


            # print self.num
            # print self.ball




        except Exception,e:
            # print(hjson)
            print(e.message)
            return False

        return True


if __name__ == '__main__':
    a = Lottery(4,2018,100)
    a.fetchdata(1)
    print(a.numsequence)
    print(a.date)

