#!/usr/bin/env python
# coding=utf-8
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
        src_file = [x for x in os.listdir(in_str)]
        src_file_list  = [os.path.join(in_str,x)for x in src_file]
        return src_file_list

    def unique(self,way,name):
        d_test2 = sorted(df7['date'].unique())
        date_to = {}
        for i in d_test2:
            temp_date = datetime.datetime.strptime(str(i),'%Y%m%d')
            n = temp_date.strftime(way)
            date_to[i] = n
            df7[name] = df7['date'].map(date_to)

    def pre_rank(self,d_test,name):
        temp_count2 = []
        for i in d_test:
            temp_df = df7[df7[name]==i]
            temp_count0 = pd.value_counts(temp_df['from'])
            temp_count1 = DataFrame(temp_count0,columns=['count'])
            temp_count1['date'] = i
            temp_count1['tel'] = temp_count1.index
            temp_count2.append(temp_count1)
        temp_count3 =pd.concat(temp_count2)
        return temp_count3
    def rank(self,df,suf,tn):
        d_test0 = sorted(df['date'].unique())
        #每个时间段
        for each_time in d_test0:
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
    def handle(self,tn):
        d_test =sorted(df7['date'].unique())
        return basic().pre_rank(d_test,'date')

class week(basic):
    def handle(self,tn):
        basic().unique('%W','week')
        d_test = sorted(df7['week'].unique())
        return basic().pre_rank(d_test,'week')

class month(basic):
    def handle(self,tn):
        basic().unique('%m','month')
        d_test = sorted(df7['month'].unique())
        return basic().pre_rank(d_test,'month')

#getopt
if __name__ =="__main__":
    '''
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
            '''
    dirs='zz_src'
    topn=5
    modes='m'
    global df7
    def summary(way):
        temp_chunk=way.handle(topn)
        chunks.append(temp_chunk)

    for each_file in basic().handle_dirs(dirs):
        reader = pd.read_csv(each_file,names=['codes','from','to','date','time','ci','lac'],iterator=True)
        loop = True
        chunkSize =1000000
        chunks=[]
        while loop:
            try:
                chunk = reader.get_chunk(chunkSize)
                df7 = chunk[chunk['date']>20000000]
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

