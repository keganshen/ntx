#!/usr/bin/env python
# coding=utf-8
import networkx as nx
import matplotlib.pyplot as plt
import csv
import datetime

G = nx.Graph()
DG = nx.DiGraph()

reader = csv.reader(file('02.csv', 'rb'))
container = []
for line in reader:
    container.append((line[1], line[2]))
G.add_edges_from(container)

#find cliques whose size is 5
result = []
print '***begin***',datetime.datetime.now()
for i in nx.enumerate_all_cliques(G):
    if len(i) == 6:
        result.append(i)
    else:
        pass
print "***done***",datetime.datetime.now()
print result

'''
apple = nx.number_strongly_connected_components(G)
strawberry = max(nx.strongly_connected_component_subgraphs(G),key=len)
try:
    watermelon = nx.find_cycle(G,orientation='ignore')
except:
    pass
for i in range(len(watermelon)):
    DG.add_edge(watermelon[i][0],watermelon[i][1])
    '''
