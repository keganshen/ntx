# -*- coding:utf-8 -*-
import getopt
import sys
import os
import numpy as np
import pandas as pd
import datetime
import csv
from pandas import Series,DataFrame
from getopt import GetoptError
#定义了一个基类，将上一版中d/w/m三种情况中类似的处理方法抽象成函数
class basic(object):
    def __init__(self):
        pass
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
            temp_dir = 'temp_count/'+suf+str(i)+'_topn.csv'
            temp_count.to_csv(temp_dir,index = True,header=False)
#去除sortn.py 在读取目录下csv文件时加上列数的判断，异常再引入处理
def handle_dirs(in_str):
    global data_dirs
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
            new_csv_name = in_str + '/'+str(count)+'_new.csv'
            reader = csv.reader(file(i,'rb'))
            writer = csv.writer(file(new_csv_name,'wb'))
            for line in reader:
                writer.writerow(list(str(line).split()))
            count += 1
            os.remove(i)
        else:
            print 'mistake occured in sourcefile!'
    data_file  = [x for x in os.listdir(in_str)]
    data_dirs =  [os.path.join(in_str,x)for x in data_file]


def handle(mode,tn):
    global df7
    global d_test
    for each_src in data_dirs:
        df5 = DataFrame(pd.read_csv(each_src,
                                   names=['codes','from','to','date','time','ci','lac']))
        df7 = df5[df5['date']>20000000]
        if mode =='d':
            d_test = sorted(df7['date'].unique())
            basic().rank(d_test,'date','d/',tn)
        if mode == 'w':
            basic().unique('%W','week')
            d_test = sorted(df7['week'].unique())
            basic().rank(d_test,'week','w/',tn)
        if mode == 'm':
            basic().unique('%m','month')
            d_test = sorted(df7['month'].unique())
            basic().rank(d_test,'month','m/',tn)
#getopt
if __name__ =="__main__":
    try:
        opts,args = getopt.getopt(sys.argv[1:],'d:t:b:')
    except GetoptError:
        sys.exit()
    for key,values in opts:
        if key in ('-d',''):
            dirs = values
        if key in ('-t',''):
            topn = values
        if key in ('-b',''):
            modes = values

handle_dirs(dirs)
handle(modes,topn)
