#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import os
import sys
import commands
Method, Calling, Called, Date, Time, Length, Location = range(0,7)

'''
要求输入的话单文件已经按主叫人升序排序
'''
def get_min_max_files(files, min_c, max_c):
    i = 0
    for each_file in files:
        output = os.popen('head -n 1 ' + each_file)
        buf = output.read()
        buf_split = buf.split(',', 2)
        #print buf_split[1]
        min_c.append(buf_split[1])

        output = os.popen('tail -n 1 ' + each_file)
        buf = output.read()
        buf_split = buf.split(',', 2)
        #print buf_split[1] + '\n'
        max_c.append(buf_split[1])

        i += 1

'''
未找到返回0
找到返回1, 并生成以account命名的csv文件
'''
def find_contacts(in_dir, account):
    print "find contacts"
    data_file = [x for x in os.listdir(in_dir)]
    data_file = sorted([os.path.join(in_dir, x) for x in data_file])
    print data_file
    min_cs = []
    max_cs = []
    get_min_max_files(data_file, min_cs, max_cs)
    print min_cs
    print max_cs

    i = 0
    found = 0
    for each_file in data_file:
        if account >= min_cs[i] and account <= max_cs[i]:
            found = 1
            break;
        i += 1
    if found == 0:
        print account + " is not found!!!"
        return 0
    print account + " maybe is in " + each_file
    (status, output) = commands.getstatusoutput('grep ' + account + ' ' + each_file)
    #print status, output
    if status != 0:
        print account + " is not found!!!"
        return 0
    print account + " is in " + each_file

    out_file = open(account + ".csv", 'w')
    out_file.write(output)
    out_file.close()
    return 1

def usage():
    print( "Usage:\n    %s <sorted file dir> <acount>" % (sys.argv[0]))

if __name__ == '__main__':
    try:
        ret = find_contacts(sys.argv[1], sys.argv[2])
    except:
        usage()
        sys.exit(0)
