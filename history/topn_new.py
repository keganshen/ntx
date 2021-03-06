#!/usr/bin/env python
# coding=utf-8
import sys
import os
import csv
import getopt
import datetime
import collections
import pandas as pd
from pandas import Series, DataFrame
from getopt import GetoptError

global df

def check_temp_file():
    a = ['temp_csv','temp_csv/d','temp_csv/w','temp_csv/m','temp_count','temp_count/d','temp_count/w','temp_count/m']
    map(lambda x:os.mkdir(x) if not (os.path.lexists(x)) else None,a)

def unique(way, name):
    unique_list = sorted(df['date'].unique())
    unique_map = {}
    for i in unique_list:
        unique_date = datetime.datetime.strptime(str(i), '%Y%m%d')
        n = unique_date.strftime(way)
        unique_map[i] = n
        df[name] = df['date'].map(unique_map)


class basic(object):
    days = []
    weeks = []
    months = []

    def __init__(self):
        pass

    def rank(self,type,name1,name2,topn):
        #每个模式下每个文件夹（如 m/04/)生成一个csv
        if type == 'd':
            target = self.days
        elif type == 'w':
            target = self.weeks
        elif type == 'm':
            target = self.months
        for each_file in target:
            n = int(topn)
            name = os.path.join(name1,str(each_file))
            month_file=[]
            for i in os.listdir(name):
                csv_name = os.path.join(name,i)
                month_file.append(csv_name)
            month_dict = {}
            month_result = {}
            count = 0
            for i in month_file:
                temp = pd.read_csv(i,header=None)
                month_dict[count] = temp.head(5)
                count += 1
            panel = pd.Panel.from_dict(month_dict,orient = 'minor')
            k = len(month_dict)
            rank_list = []
            rank_deep = []
            for i in range(k):
                rank_list.append(int(panel[1][:1][i]))
            while n:
                a = rank_list.index(max(rank_list))
                e = panel[0][a][collections.Counter(rank_deep)[a]]
                f =  [panel[1][a][collections.Counter(rank_deep)[a]]]
                month_result[e]=f
                rank_deep.append(a)
                try:
                    b = int(panel[1][a][collections.Counter(rank_deep)[a]])
                except:
                    b = 0
                del rank_list[a]
                rank_list.insert(a,b)
                n -= 1
            out_name = os.path.join(name2,''.join((str(each_file),'.csv')))
            DataFrame(month_result).T.sort(columns = 0,ascending=False).to_csv(out_name,index=True,header=False)
        print '***done***',datetime.datetime.now()

class byday(basic):
    def day(self,n):
        day_list = sorted(df['date'].unique())
        for i in day_list:
            if i not in self.days:
                self.days.append(i)
            if os.path.lexists(os.path.join('temp_csv/d', str(i))):
                pass
            else:
                os.mkdir(os.path.join('temp_csv/d', str(i)))
            day_df = df[df['date'] == i]
            day_c = pd.value_counts(day_df['from'])
            name = os.path.join('temp_csv/d', str(i), ''.join((str(n), '.csv')))
            day_c.to_csv(name, index=True, header=False)

class byweek(basic):
    def week(self,n):
        unique('%W', 'week')
        week_list = sorted(df['week'].unique())
        for i in week_list:
            if i not in self.weeks:
                self.weeks.append(i)
            if os.path.lexists(os.path.join('temp_csv/w',str(i))):
                pass
            else:
                os.mkdir(os.path.join('temp_csv/w',str(i)))
            week_df = df[df['week'] == i]
            week_c = pd.value_counts(week_df['from'])
            name = os.path.join('temp_csv/w',str(i),''.join((str(n),'.csv')))
            week_c.to_csv(name,index=True,header=False)

class bymonth(basic):
    def month(self,n):
        unique('%m', 'month')
        month_list = sorted(df['month'].unique())
        for i in month_list:
            if i not in self.months:
                self.months.append(i)
            if os.path.lexists(os.path.join('temp_csv/m',str(i))):
                pass
            else:
                os.mkdir(os.path.join('temp_csv/m',str(i)))
            month_df = df[df['month'] == i]
            month_c = pd.value_counts(month_df['from'])
            name = os.path.join('temp_csv/m',str(i),''.join((str(n),'.csv')))
            month_c.to_csv(name,index=True,header=False)

def help_info():
    print '********\n help doc \n command: python topn_get.py -d -t -b -h -v \n ***-d*** 存放带分析的csv文件目录. \n ***-t*** 需要分析初前多少名 \n ***-b*** 分析的方式 d/w/m(天/周/月) \n ***-h*** help \n ***-v*** 版本\n********'


if __name__=="__main__":
    check_temp_file()
    try:
        opts,args = getopt.getopt(sys.argv[1:],'d:t:b:hv')
    except GetoptError:
        sys.exit()
    for key,values in opts:
        if key in ('-d',''):
            s_dir = values
        if key in ('-t',''):
            topn = values
        if key in ('-b',''):
            modes = values
        if key in ('-h',''):
            help_info()
            sys.exit()
        if key in ('-v',''):
            print '0.0.1'
            sys.exit()

    print '***split begin***',datetime.datetime.now()
    for root, dirs, files in os.walk(s_dir):
        count_sort_file = 0
        for i in files:
            path_i = os.path.join(os.getcwd(), s_dir, i)
            reader = pd.read_csv(
                path_i,
                names=['codes','from','to','date','time','ci','lac'])
            df = reader[reader['date'] > 20000000]
            if modes == 'd':
                byday().day(count_sort_file)
            if modes == 'w':
                byweek().week(count_sort_file)
            if modes == 'm':
                bymonth().month(count_sort_file)
            count_sort_file += 1
    print '***split done***',datetime.datetime.now()
    if modes == 'd':
        basic().rank('d','temp_csv/d','temp_count/d',topn)
    if modes == 'w':
        basic().rank('w','temp_csv/w','temp_count/w',topn)
    if modes == 'm':
        basic().rank('m','temp_csv/m','temp_count/m',topn)
