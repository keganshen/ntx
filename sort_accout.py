#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import re
import os
import sys
import csv
import commands
import datetime
import distutils.dir_util
#########################################################
import list_csv
Method, Calling, Called, Date, Time, Length, Location = range(0,7)


split_num = 5
csv_fds = []
output_files1 = []
line_limit = 100000
null_line_num = 0

def create_readers(input_dir):
    # get all csv files name
    global csv_fds
    csv_list = list_csv.list_csv(input_dir)
    print csv_list
    # create csv readers
    csv_readers = []
    for i in csv_list:
        i = os.path.join(input_dir, i)
        #print i
        try:
            fd = open(i, "r")
            csv_fds.append(fd)
        except Exception as e:
            print(e)
            sys.exit(0)
        csv_reader = csv.reader((','.join(line.split()) \
                     for line in fd), delimiter=',')
        #for row in csv_reader:
        #    new_item = tuple(row)
        #    print new_item
        #    new_item1 = row[0]
        #    new_item2 = row[1]
        #    print new_item1 + new_item2
        csv_readers.append(csv_reader)
    return csv_readers

def create_writers_readers(output_dir):
    global output_files1
    # create csv writers
    csv_writers = []
    csv_readers = []
    for i in range(0, split_num):
        out_file = os.path.join(output_dir, "sort_account" + str(i) + ".txt")
        try:
            fd = open(out_file, "w+")
            output_files1.append(fd)
        except Exception as e:
            print(e)
            sys.exit(0)
        csv_writer = csv.writer(fd, delimiter=',',lineterminator='\n')
        csv_writers.append(csv_writer)
        csv_readers.append(csv.reader(fd,delimiter=','))
    return csv_writers, csv_readers

def write_hash_file(buf, csv_writers, max_cs):
    writer_num = len(csv_writers)
    buf_num = len(buf)
    line_per_file = (buf_num + split_num - 1) / writer_num
    #print "len per file:", line_per_file
    idx = i = j = 0
    #print max_cs
    #hash algr1
    '''
    for line in buf:
        j = hash(str(line[Calling])) % split_num
        csv_writers[j].writerow(line)
    '''
    #hash algr2
    '''
    for line in buf:
        j = hash(str(line[Calling])) % split_num
        csv_writers[j].writerow(line)
    '''
    #hash algr3
    if len(max_cs) == 0:
        max_cs += ['0'] * split_num
        for line in buf:
            #print line
            if i >= line_per_file and buf[idx-1][Calling] != buf[idx][Calling]:
                # the last file never update maximum, always '99999'
                if j < split_num:
                    max_cs[j] = buf[idx-1][Calling]
                j += 1
                i = 0
            if idx == buf_num -1:
                #print max_cs + j + idx + buf[idx][Calling]
                max_cs[j] = buf[idx][Calling]
            csv_writers[j].writerow(line)
            i += 1
            idx += 1
    else:
        for line in buf:
            if line[Calling] > max_cs[j]:
                if j < split_num - 1:
                    j += 1
                    i = 0
                else:
                    max_cs[j] = line[Calling]
            csv_writers[j].writerow(line)
            i += 1
            idx += 1
    #print max_cs

def get_line_limit(csv_readers, num = 0, file_end = 0):
    global null_line_num
    buf = []
    reader_num = len(csv_readers)
    #print reader_num
    i = j = 0
    while True:
        try:
            line = csv_readers[j].next()
            if line:
                buf.append(line)
                i += 1
            else:
                null_line_num += 1
            #buf.append(csv_readers[j].next())
        except:
            if j < reader_num -1:
                j += 1
                if file_end:
                    yield buf
                    buf = []
                    i = 0
                continue
            else:
                yield buf
                return
        if num == 0 or i < num:
            continue
        yield buf
        i = 0
        buf = []

def sort_data(in_str, out_str):
    print 'sort data!'
    try:
        cwd = os.getcwd()
        input_dir = os.path.join(cwd, in_str)
        output_dir = os.path.join(cwd, out_str)

        # check dirs
        if not os.path.isdir(input_dir):
            print("input_dir is not directory")
            os.exit(-1)
        if not os.path.isdir(output_dir):
            distutils.dir_util.mkpath(output_dir)
    except:
        print("exit")
        sys.exit(-1)

    '''
    首先读取line_limit行数的块，排序后散列到split_num个文件中
    '''
    print "Begin hash file, time: ", datetime.datetime.now()
    max_callings = []
    csv_readers = create_readers(input_dir)
    gen_buf0 = get_line_limit(csv_readers, line_limit, 0)
    csv_writers1, csv_readers1  = create_writers_readers(output_dir)
    while True:
        try:
            buf = gen_buf0.next()
            buf.sort(key = lambda k:k[Calling], reverse = False)
            #print "this time is:", len(buf)
            write_hash_file(buf, csv_writers1, max_callings)
        except:
            print("Read End")
            break
    for f in csv_fds:
        f.close()
    for f in output_files1:
        f.close()
    print "End hash file, time: ", datetime.datetime.now()
    print "null_line_num", null_line_num

    print "Begin sort every file, time: ", datetime.datetime.now()
    out_files = os.listdir(output_dir)
    for f in out_files:
        portion = os.path.splitext(f)
        if portion[1] != ".txt":
            continue
        old_name = output_dir + f
        new_name = output_dir + portion[0] + ".csv"
        (status, output) = commands.getstatusoutput('sort -k 2 -t "," ' + old_name + ' -S 2G -o ' + new_name)
        if status == 0:
            (status, output) = commands.getstatusoutput('rm -f ' + old_name)
    print "End sort every file, time: ", datetime.datetime.now()

def usage():
    print( "Usage:\n    %s <src dir> <sorted dir>" % (sys.argv[0]))

if __name__ == '__main__':
    try:
        sort_data(sys.argv[1], sys.argv[2])
    except:
        usage()
        sys.exit(0)

