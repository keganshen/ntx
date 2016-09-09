#!/usr/bin/env python
# coding=utf-8
import getopt
import sys
import os
import numpy as np
import pandas as pd
import datetime
import csv
from pandas import Series,DataFrame
from getopt import GetoptError

class basic(object):
    data_dirs =None
    d_test =None
    def __init__(self):
        pass
    def handle_dirs(self,in_str):
        try:
            cwd = os.getcwd()
            input_dir = os.path.join(cwd,in_str)
            #check dirs
            if not os.path.isdir(input_dir):
                print 'input_dir is not directory'
                os.exit(-1)
        except:
            sys.exit(-1)
        data_file0 = [x for x in os.listdir(in_str)]
        data_dirs0 = [os.path.join(in_str,x)for x in data_file0]
        count = 0
        for i in data_dirs0:
            df0 = DataFrame(pd.read_csv(i))
        #检查原CSV文件的列数，正常有七列，处理只有一列时的异常
        if len(df0.columns)==7:
            pass
        elif len(df0.columns)==1:
            new_csv_name0 = [str(count),'_new.csv']
            new_csv_name1 = ''.join(new_csv_name0)
            new_csv_name = os.path.join(in_str,new_csv_name1)
            reader = csv.reader(file(i,'rb'))
            writer = csv.writer(file(new_csv_name,'wb'))
            for line in reader:
                writer.writerow(list(str(line).split()))
            count += 1
            os.remove(i)
        else:
            print 'mistake occured in sourcefile!'
        data_file  = [x for x in os.listdir(in_str)]
        self.data_dirs =  [os.path.join(in_str,x)for x in data_file]
        return self.data_dirs

    def unique(self,way,name):
        d_test2 = sorted(df7['date'].unique())
        date_to={}
        for i in d_test2:
            temp_date = datetime.datetime.strptime(str(i),'%Y%m%d')
            n = temp_date.strftime(way)
            date_to[i]=n
            df7[name]=df7['date'].map(date_to)

    def rank(self,d_test,name,suf,tn):
        for i in d_test:
            temp_df = df7[df7[name] == i]
            temp_count0 = pd.value_counts(temp_df['from'])
            temp_count = DataFrame(temp_count0[0:int(tn)],columns=['degree'])
            temp_dir0 = [str(i),'_topn.csv']
            temp_dir = os.path.join('temp_count',suf,''.join(temp_dir0))
            temp_count.to_csv(temp_dir,index = True,header=False)

class day(basic):
    def handle(self,tn):
        d_test =sorted(df7['date'].unique())
        basic().rank(d_test,'date','d',tn)

class week(basic):
    def handle(self,tn):
        basic().unique('%W','week')
        d_test = sorted(df7['week'].unique())
        basic().rank(d_test,'week','w',tn)

class month(basic):
    def handle(self,tn):
        basic().unique('%m','month')
        d_test = sorted(df7['month'].unique())
        basic().rank(d_test,'month','m',tn)

#getopt
if __name__ =="__main__":
    try:
        opts,args = getopt.getopt(sys.argv[1:],'d:t:b:')
    except GetoptError:
        sys.exit()
    for key,values in opts:
        '''
        if key in ('-d',''):
            dirs = values
        if key in ('-t',''):
            topn = values
        if key in ('-b',''):
            modes = values
            '''
dirs ='zz_src'
topn = 5
modes ='d'
global df7

for each_src in basic().handle_dirs(dirs):
    df5 = DataFrame(pd.read_csv(each_src,
                                names = ['codes','from','to','date','time','ci','lac']))
    df7 = df5[df5['date']>20000000]
    if modes == 'd':
        day().handle(topn)
    if modes == 'w':
        week().handle(topn)
    if modes == 'm':
        month().handle(topn)
