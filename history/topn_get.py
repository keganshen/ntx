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

def handle_d(in_str):
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
        #检查原CSV文件的列数，正常为7，处理1的异常
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

def handle_b(b,n):
    global df7
    global d_test
    #对文件下每个CSV操作
    for each_src in data_dirs:
        df5 = DataFrame(pd.read_csv(each_src,
                            names=['code','from','to','date','time','ci','lac']))
        #去除一些错误条目
        df7 = df5[df5['date']>20000000] 
         #每天
        if modes == 'd':
            #列出唯一的日期
            d_test = sorted(df7['date'].unique()) 
            for i in d_test:
                #从信息源筛选出每一天的信息
                temp_df = df7[df7['date'] == int(i)]
                #按拨出次数排名
                temp_count0 = pd.value_counts(temp_df['from'])
                #选出前n名
                temp_count  = DataFrame(temp_count0[0:int(n)],columns=['degree'])
                #增加第三列（日期），导出csv
                temp_count['when'] = int(i)
                temp_dir = 'temp_count/d/'+str(i)+'_topn.csv'
                temp_count.to_csv(temp_dir,index = True,header=False)
            print 'done'
         #每周
        if modes == 'w':
            d_test2=sorted(df7['date'].unique())
            date_to_week={}
            for i in d_test2:
                #根据日期获取该日期在一年的第几周
                temp_date = datetime.datetime.strptime(str(i),"%Y%m%d")
                n = temp_date.strftime('%W')
                #添加映射
                date_to_week[i]=n
            #从日期映射到第几周
            df7['week']=df7['date'].map(date_to_week)
            #列出唯一的周数
            d_test = sorted(df7['week'].unique())
            for i in d_test:
                temp_df = df7[df7['week'] == i]
                temp_count0 = pd.value_counts(temp_df['from'])
                temp_count  = DataFrame(temp_count0[0:int(n)],columns=['degree'])
                temp_count['when'] = '第'+str(i)+'周'
                temp_dir = 'temp_count/w/'+str(i)+'_topn.csv'
                temp_count.to_csv(temp_dir,index = True,header=False)
                print 'Done'
         #每月
        if modes == 'm':
            d_test2=sorted(df7['date'].unique())
            date_to_month={}
            for i in d_test2:
                temp_date = datetime.datetime.strptime(str(i),"%Y%m%d")
                n = temp_date.strftime('%m')
                date_to_month[i]=n
            df7['month']=df7['date'].map(date_to_month)
            d_test = sorted(df7['month'].unique())
            for i in d_test:
                temp_df = df7[df7['month']== i]
                temp_count0 = pd.value_counts(temp_df['from'])
                temp_count  = DataFrame(temp_count0[0:int(n)],columns=['degree'])
                temp_count['when'] = '第'+str(i)+'月'
                temp_dir = 'temp_count/m/'+str(i)+'_topn.csv'
                temp_count.to_csv(temp_dir,index = True,header=False)
                print 'donE'
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

handle_d(dirs)
handle_b(modes,topn)
