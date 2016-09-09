#!/usr/bin/env python2.7
# -*- coding:utf-8 -*-
import os
import sys
import csv
import distutils.dir_util

def list_csv(input_dir):
    csv = []
    try:
        files = os.listdir(input_dir)
    except:
        return csv

    for i in files:
        if i[0] == '.':
            continue
        if len(i) < 3:
            continue
        if i[-4:] == '.csv':
            csv.append(i)
    return csv