import csv
import math
import scipy as sp
import matplotlib 
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 
import datetime
import networkx as nx

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from modules import *


#### databeses from NYC open city dataset

T = pd.read_csv('ManhattanTree.csv')
c= T.columns()


# <0 TREEID> <1 OBJECTID_1> <2 ONSTREET> <3 PARITY> <4 CROSSSTREE>, < 5 CROSSSTR_1> <6 BUILDINGNU> <7 BUILDINGST> < 8 TREELOCATI> <9 SITE> < 10 TREEPIT> <11 TREECONDIT> < 12 DIAMETER> < 13 SPECIES> < 14 BOROUGH> <15 ZIPCODE> <16 FID_1> < 17 COMMDIST>

sxx = get_sxx(T)


#deal with 113 trees with not listed info!
# esentially adds at least 6 more images. 

nl = 0
nP = 0
for i in keys:
    if 'not listed' in i:
        nl = nl +sxx[i]['tree_count']
        nP=nP +1
        for j in range(sxx[i]['tree_count']):
            print T[T[c[0]]==sxx[i]['tree_id'][j]]['BUILDINGST']
            



