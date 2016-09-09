#!/usr/bin/env python
# coding=utf-8
import csv 

reader=csv.reader(file('../new_account.csv','rb'))
writer = csv.writer(file('../zz_src/02.csv','wb'))

for line in reader:
    for i in range(18):
        writer.writerow(line)

