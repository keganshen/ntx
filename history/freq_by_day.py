#!/usr/bin/env python2.7
# -*- coding:utf-8 -*-
import os
import csv
import getopt
import sys
from getopt import GetoptError

#python freq_by_day.py -a TELNUM

#获取相关的数据
def extract_data(tel_num):
    temp_name =str(tel_num)+'.csv'
    reader = csv.reader(file(temp_name,'rb'))

    time_hour =[]
    days = []
    for line in reader:
        time_hour.append(line[4])
        days.append(line[3])
    if (len(days)==0 or len(time_hour)==0):
        return (0,time_hour,days)
    else:
        return (1,time_hour,days)

#处理 算出每天的平均数据，导出
def avg(tel_num):
    count = [[ 0 for row in range(2)] for col in range (24)]
    for i in range(25):
        count[i-1][0] =i

    time_hour = extract_data(tel_num)[1]
    days = extract_data(tel_num)[2]
    select_days = []

    for i in range(len(time_hour)):
        t = int(time_hour[i][0]+time_hour[i][1])
        count[t-1][1] +=1
    for i in days:
        if i not in select_days:
            select_days.append(i)

    for i in range(25):
        count[i-1][1] = count[i-1][1] / float(len(select_days))

    save_name = str(tel_num)+'.day.csv'
    writer =csv.writer(file(save_name,'wb'))
    for line in count:
        writer.writerow(line)
    if os.path.exists(save_name):
        return 1

#getopt
try:
    opts,args = getopt.getopt(sys.argv[1:],'a:')
except GetoptError:
    sys.exit()
for key,values in opts:
    if key in ('-a',''):
        tel_num = values
        avg(tel_num)
