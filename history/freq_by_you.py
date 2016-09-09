# -*- coding:utf-8 -*-
import os
import csv
import getopt
import sys
from getopt import GetoptError
import datetime
#python freq_by_you.py -a TEL -b x       (x可以是 d 生成.day.csv文件，也可以时 w 生成.week.csv文)

class basic(object):
    def __init__(self,tel_num=None):
        self.tel_num = tel_num
    #生成初始表格
    def initial_form(self,ccol):
        count = [[ 0 for row in range (2)]for col in range(ccol)]
        for i in range(ccol+1):
            count[i-1][0]=i
        return count
    #从tel_num.csv文件中获取时间信息
    def get_data(self):
        temp_name = str(self.tel_num)+'.csv'
        reader = csv.reader(file(temp_name,'rb'))
        time_hour = []
        days = []
        for line in reader:
            time_hour.append(line[4])
            days.append(line[3])
        return (time_hour,days)
    #写成csv文档
    def write_csv(self,count,save_name):
        writer =csv.writer(file(save_name,'wb'))
        for line in count:
            writer.writerow(line)

#天规律
class by_day(basic):
    def handle(self):
        #调用父类，生成初始表格
        count = basic().initial_form(24)
        #调用父类，获取时间信息
        time_hour = basic(tel_num).get_data()[0]
        days = basic(tel_num).get_data()[1]
        select_days = []
        #初计算
        for i in range(len(time_hour)):
            t = int(time_hour[i][0]+time_hour[i][1])
            count[t-1][1] +=1
        for i in days:
            if i not in select_days:
                select_days.append(i)
        #计算平均值
        for i in range(25):
            count[i-1][1] = count[i-1][1] / float(len(select_days))
        #调用父类，写成csv
        save_name = str(tel_num)+'.day.csv'
        basic(tel_num).write_csv(count,save_name)
        return 0

#周规律
class by_week(basic):
    def handle(self):
        #调用父类，生成初始表格
        count = basic().initial_form(7)
        #调用父类，获取时间信息(days)
        days=basic(tel_num).get_data()[1]
        weekdays = []
        #初计算
        for i in days:
            weekday = datetime.datetime(int(i[0:4]),int(i[4:6]),int(i[6:8])).strftime("%w")
            weekdays.append(int(weekday))
        for i in weekdays:
            if i == 0 :
                count[6][1] += 1
            else:
                count[i-1][1] +=1
        #计算平均值
        a = datetime.date(int(days[0][0:4]),int(days[0][4:6]),int(days[0][6:8])).isocalendar()
        b = datetime.date(int(days[-1][0:4]),int(days[-1][4:6]),int(days[-1][6:8])).isocalendar()
        c = b[1]-a[1]+1

        for i in range(7):
            count[i][1] /= float(c)
            count[i][1] = round(count[i][1],2)
        #调用父类，写成csv
        save_name = str(tel_num)+'.week.csv'
        basic(tel_num).write_csv(count,save_name)


#根据传参决定实例化对象
def decision(tel_num,way):
    if way == 'd':
        by_day(tel_num).handle()
    elif way == 'w':
        by_week(tel_num).handle()

way=None
tel_num = None
if __name__ =="__main__":
#getopt
    try:
        opts,args = getopt.getopt(sys.argv[1:],'a:b:')
    except GetoptError:
        sys.exit()
    for key,values in opts:
        if key in ('-a',''):
            tel_num = values
        if key in ('-b',''):
            way = values
    decision(tel_num, way)
