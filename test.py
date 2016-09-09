#!/usr/bin/env python
# coding=utf-8
import os
import pandas as pd
import pandas.io.data as web

a = [1,2,3,5,7,9]
b = []
b.append(a[0])
del a[0]
c = 0
d = 1

if not c == 1 and d == 1:
    e = a.pop()
    print a
    print e
