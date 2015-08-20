import csv
import math
import scipy as sp
import numpy as np
import pandas as pd 
import datetime

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import networkx as nx
from networkx.readwrite import json_graph
import json 
import geopandas as gpd


from dateutil import parser


def get_sxx(T):
    sxx = {}
    for i in range(len(T)):
        key = '%s, %s, %s' %(T[c[2]][i], T[c[4]][i],T[c[5]][i])
        keysalt = '%s, %s, %s' %(T[c[2]][i], T[c[5]][i],T[c[4]][i])
        if sxx.has_key(key)==False and sxx.has_key(keysalt)==False:
            sxx[key] = {}
            sxx[key]['tree_count'] = 1
            sxx[key]['tree_id'] = [T[c[0]][i]]
        else:
            if sxx.has_key(key) and key!=keysalt:
                sxx[key]['tree_count'] = sxx[key]['tree_count'] + 1
                sxx[key]['tree_id'].append(T[c[0]][i])
            else:
                sxx[keysalt]['tree_count'] = sxx[keysalt]['tree_count'] + 1
                sxx[keysalt]['tree_id'].append(T[c[0]][i])
    return sxx


def list_XinColumn(T, c):
    X = []
    for i in T[c]:
        if i not in X:
            X.append(i)
    return X







