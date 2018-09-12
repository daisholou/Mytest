# -*- coding: UTF-8 -*-
import urllib2
import demjson as json

class Lottery():
    def __init__(self,tp,year,term):
        self.num = {} # 球号
        self.tp = tp   #体彩中心彩票类型 大乐透是4
        self.year = year #年份。如2018
        self.term = term
        self.id = (year%100)*1000+term #期号
        self.num = {} # 球号
        self.numsequence = '' #读取的球号数据
        self.date = '' #日期
        self.ball = 0
    def FetchData(self):
 #使用的是哪一套摇奖球
        try:
            thisterm = str(self.id)

            url = "http://www.lottery.gov.cn/api/lottery_kj_detail_new.jspx?_ltype=%s&_term=%s" % (self.tp, thisterm)

            html = urllib2.urlopen(url)

            hjson = json.decode(html.read())

            if not hjson[0]:
                return False

            self.numsequence = hjson[0]['lottery']['numSequence']
            self.num['r1'] = self.numsequence[0:2]
            self.num['r2'] = self.numsequence[3:5]
            self.num['r3'] = self.numsequence[6:8]
            self.num['r4'] = self.numsequence[9:11]
            self.num['r5'] = self.numsequence[12:14]
            self.num['b1'] = self.numsequence[15:17]
            self.num['b2'] = self.numsequence[18:20]
            self.ball = int(self.numsequence[27])

            # print self.num
            # print self.ball

            self.date = hjson[0]['lottery']['openTime_fmt1']


        except Exception:
            print('Error:'+Exception)
            return False


        return True

if __name__ == '__main__':

    a = Lottery(4,2018,100)
    a.FetchData()
    print(a.numsequence)
    print(a.date)

