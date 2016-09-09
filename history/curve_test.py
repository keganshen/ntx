#coding=utf-8
import getopt
from getopt import GetoptError
import unittest
import os
import sys
from curve_get import by_day,by_week
import csv
import datetime
import random


class Test_fby(unittest.TestCase):
    TEL = None
    WAY = None
    TYPE = None
    now = 20160704
    store_w = []
    store_r = []
    def get_data(self,h):
        h0 = h
        while h0>0:
            self.store_w.append(self.now+h)
            h0 -= 1
    #天
    def setUp(self):
        if self.WAY == 'd' :
            if self.TYPE == 'inc':
                for i in range(25):
                    i0 = i
                    while i0 > 0:
                        self.store_w.append(i*10000)
                        i0 -= 1
            elif self.TYPE == 'dec':
                for i in range(25):
                    i0 =i
                    while i0 > 0:
                        self.store_w.append((25-i)*10000)
                        i0 -= 1
            elif self.TYPE == 'random':
                self.store_r = [0 for i2 in range(24)]
                for i in range(24):
                    i1 = random.randint(1,5)
                    self.store_r[i] +=i1
                    for i3  in range(i1):
                        self.store_w.append((i+1)*10000)
            else:
                print '未制定正确的处理方式!'
        #天
            temp_l = [[0 for row in range(24)] for col in range(len(self.store_w))]
            for i in range(len(temp_l)):
                temp_l[i][0] = 570
                temp_l[i][1] = self.TEL
                temp_l[i][3] = 20160728
                temp_l[i][4] = self.store_w[i]
        #周
        if self.WAY == 'w':
            if self.TYPE == 'inc':
                for i in range(8):
                    i0 =i
                    while i0 > 0:
                        self.store_w.append(self.now+i-1)
                        i0 -= 1
            elif self.TYPE == 'dec':
                for i in range(8):
                    i0 = i
                    while i0 >0:
                        self.store_w.append(self.now+7-i)
                        i0 -=1
            elif self.TYPE == 'random':
                self.store_r = [0 for i2 in range(7)]
                for i in range(7):
                    i1 = random.randint(1,10)
                    self.store_r[i] +=i1
                    for i3 in range(i1):
                        self.store_w.append(i+self.now)
        #周
            temp_l =[[0 for row in range(7)] for col in range(len(self.store_w))]
            for i in range(len(temp_l)):
                temp_l[i][0] = 570
                temp_l[i][1] = self.TEL
                temp_l[i][3] = self.store_w[i]
                temp_l[i][4] = random.randint(0,240000)

        temp_n =self.TEL +'.csv'
        writer = csv.writer(file(temp_n,'wr'))
        for i in range(len(temp_l)):
            writer.writerow(temp_l[i])

        print '----------------生成了.csv文件-----------------'
    def tearDown(self):
        pass
    def test_by_day(self):
        print '*********'
        if self.WAY=='d':
            tt=[]
            tp=[]
            by_day(self.TEL).handle()
            tn = self.TEL+".day.csv"
            reader = csv.reader(file(tn,'rb'))
            for line in reader:
                tp.append(float(line[1]))
            for i in range(24):
                tt.append(float(i+1))
            if self.TYPE == 'inc':
                 pass
            elif self.TYPE == 'dec':
                tt.reverse()
            elif self.TYPE == 'random':
                tt = self.store_r
            print '----------------准备测试----------------'
            self.assertEquals(tt,tp)
            print '----------------完成测试----------------'
        elif self.WAY == 'w':
            tt=[]
            tp=[]
            by_week(self.TEL).handle()
            tn = self.TEL+".week.csv"
            reader = csv.reader(file(tn,'rb'))
            for line in reader:
                tp.append(float(line[1]))
            for i in range(7):
                tt.append(float(i+1))
            if self.TYPE == 'inc':
                 pass
            elif self.TYPE == 'dec':
                tt.reverse()
            elif self.TYPE == 'random':
                tt = self.store_r
            print '----------------准备测试----------------'
            self.assertEquals(tt,tp)
            print '----------------完成测试----------------'
if __name__ == "__main__":
    if len(sys.argv) > 1:
        Test_fby.TYPE= sys.argv.pop()
        Test_fby.WAY = sys.argv.pop()
        Test_fby.TEL = sys.argv.pop()
    unittest.main()
