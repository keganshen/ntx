#!/usr/bin/env python2.7
# -*- coding:utf-8 -*-
import os
import csv
import getopt
import sys
from getopt import GetoptError
import datetime

#python freq_by_week.py -a TELNUM
#获取相关数据
def extract_data(tel_num):
    temp_name =str(tel_num)+'.csv'
    reader = csv.reader(file(temp_name,'rb'))

    days = []
    days0 = []
    for line in reader:
        days.append(line[3])

#for循环 改变i值 不会存在原列表？
#0代表周日，1-6为周一到周六
    for i in days:
        weekday = datetime.datetime(int(i[0:4]),int(i[4:6]),int(i[6:8])).strftime("%w")
        days0.append(int(weekday))
    if len(days)!=0 and (days0)!=0:
        return (1,days,days0)
    else:
        return (0,days,days0)

def avg(tel_num):
    count = [[ 0 for row in range(2)] for col in range (7)]
    for i in range(8):
        count[i-1][0] =i
    days0=extract_data(tel_num)[2]
    days = extract_data(tel_num)[1]

    for i in days0:
        if i==0:
            count[6][1] +=1
        else:
            count[i-1][1] +=1
#how many weeks
    a = datetime.date(int(days[0][0:4]),int(days[0][4:6]),int(days[0][6:8])).isocalendar()
    b = datetime.date(int(days[-1][0:4]),int(days[-1][4:6]),int(days[-1][6:8])).isocalendar()
    c = b[1]-a[1]+1

    for i in range(7):
        count[i][1] /= float(c)
        count[i][1] = round(count[i][1],2)

    save_name = str(tel_num)+'.week.csv'
    writer = csv.writer(file(save_name,'wb'))
    for line in count:
        writer.writerow(line)
    if os.path.getsize(save_name)!=0:
        return 1
    else:
        return 0

#getopt
try:
    opts,args = getopt.getopt(sys.argv[1:],'a:')
except GetoptError:
    sys.exit()
for key,values in opts:
    if key in ('-a',''):
        tel_num = values
        avg(tel_num)
