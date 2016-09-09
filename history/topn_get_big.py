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
    data_dirs = None
    d_test = None
    def __init__(self):
        pass
    def csv_list(self,in_str):
        try:
            cwd = os.getcwd()
            input_dir = os.path.join(cwd,in_str)
            #check dirs
            if not os.path.isdir(input_dir):
                print 'input_dir is not directory'
                os.exit(-1)
        except:
            sys.exit(-1)
        src_file = [x for x in os.listdir(in_str)]
        src_file_list  = [os.path.join(in_str,x)for x in src_file]
        return src_file_list

    def unique(self,way,name):
        unique_list = sorted(df7['date'].unique())
        u_map = {}
        for i in unique_list:
            temp_date = datetime.datetime.strptime(str(i),'%Y%m%d')
            n = temp_date.strftime(way)
            u_map[i] = n
            df7[name] = df7['date'].map(u_map)

    def pre_rank(self,d_test,name):
        p_container = []
        for i in d_test:
            temp_df = df7[df7[name]==i]
            series_rank = pd.value_counts(temp_df['from'])
            p_df = DataFrame(series_rank,columns=['count'])
            p_df['date'] = i
            p_df['tel'] = p_df.index
            p_container.append(p_df)
        p_sum =pd.concat(p_container)
        return p_sum
    def rank(self,df,suf,tn):
        rank_list = sorted(df['date'].unique())
        #每个时间段
        for each_time in rank_list:
            temp_count3 = df[df['date']==each_time]
            d_test3 = temp_count3['tel'].unique()
            rank_dict={}
            #每个号码
            for i in d_test3:
                rank_dict[i] = temp_count3[temp_count3['tel']==i]['count'].sum()
            df3 = Series(rank_dict).order()[-int(tn):]
            df4 = DataFrame(df3,columns=['count'])
            temp_dir0 = [str(each_time),'_test.csv']
            temp_dir = os.path.join('temp_count',suf,''.join(temp_dir0))
            df4.to_csv(temp_dir,index = True,header=False)
        print '***rank done***'

class day(basic):
    def handle(self):
        d_test =sorted(df7['date'].unique())
        return basic().pre_rank(d_test,'date')

class week(basic):
    def handle(self):
        basic().unique('%W','week')
        d_test = sorted(df7['week'].unique())
        return basic().pre_rank(d_test,'week')

class month(basic):
    def handle(self):
        basic().unique('%m','month')
        d_test = sorted(df7['month'].unique())
        return basic().pre_rank(d_test,'month')

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
    global df7
    def summary(way):
        temp_chunk=way.handle()
        chunks.append(temp_chunk)

    for each_file in basic().csv_list(dirs):
        reader = pd.read_csv(each_file,names=['codes','from','to','date','time','ci','lac'],iterator=True)
        loop = True
        chunkSize =1000000
        chunks=[]
        container1 = []
        while loop:
            try:
                chunk = reader.get_chunk(chunkSize)
                for i in range(chunkSize):
                    lister0 = chunk['codes'][i].split()
                    container1.append(lister0)
                df1 = DataFrame(container1,columns=['codes','from','to','date','time','ci','lac'])
                print '***conversion done***'
                df7 = df1[df1['date']>20000000]
                if modes == 'd':
                    summary(day())
                if modes == 'w':
                    summary(week())
                if modes == 'm':
                    summary(month())
            except StopIteration:
                loop = False
                print 'Iteration is stopped'
        df = pd.concat(chunks)
        print '***sum done***'
        if modes == 'd':
            basic().rank(df,'d',topn)
        if modes == 'w':
            basic().rank(df,'w',topn)
        if modes == 'm':
            basic().rank(df,'m',topn)
