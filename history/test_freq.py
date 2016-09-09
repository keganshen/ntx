#coding=utf-8
import getopt
from getopt import GetoptError
import unittest
import os
import sys
from try_test import by_day,by_week
import csv
import datetime

#这份测试代码用的unittest，除了断言其他都没写死，但是我觉得这样测试比较复杂，因为自己要构建用于测试的对照组（这就多了一段代码）。
#python test_freq_by_you.py TEL x (TEL 随意输入号码，x 可输入 d 或 w，输入d测试by_day，输入w测试by_week.

class Test_fby(unittest.TestCase):
    TEL = None
    WAY = None
    now = datetime.datetime.now()
    def setUp(self):
        nows =datetime.datetime.strftime(self.now,'%Y-%m-%d %H-%M-%S')
        temp_w =nows[:4]+nows[5:7]+nows[8:10]
        temp_d =nows[11:13]+nows[14:16]+nows[17:19]

        temp_l =[0 for row in range(7)]
        temp_l[1] = self.TEL
        temp_l[3] = temp_w
        temp_l[4] = temp_d
        temp_n =self.TEL +'.csv'
        writer = csv.writer(file(temp_n,'wr'))
        writer.writerow(temp_l)
        return nows[11:13]
    def tearDown(self):
        pass

    def test_by_day(self):
        if self.WAY=='d':
            by_day(self.TEL).handle()
            tn = self.TEL+".day.csv"
            reader = csv.reader(file(tn,'rb'))
            tp = []
            for line in reader:
                tp.append(line[1])
            n =int(self.now.strftime('%H'))
            self.assertEquals(tp[n-1],'1.0')
        elif self.WAY=='w':
            by_week(self.TEL).handle()
            tn = self.TEL+".week.csv"
            reader = csv.reader(file(tn,'rb'))
            tp=[]
            for line in reader:
                tp.append(line[1])
            n = int(self.now.strftime('%w'))
            self.assertEquals(tp[n-1],'1.0')
        print '------end--------'

if __name__ == "__main__":
    if len(sys.argv) > 1:
        Test_fby.WAY = sys.argv.pop()
        Test_fby.TEL = sys.argv.pop()
    unittest.main()

