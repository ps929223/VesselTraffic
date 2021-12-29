
import os, sys
sys.path.append('D:/programming/SatModel/Lib')
from lib_os import *
import Map as Map
import pandas as pd
import Lib.lib_shiptype as st
import matplotlib.pyplot as plt
import numpy as np

path_ais='E:/03_MarineTraffic/위성연계해경/ais2018_DS'
path_out_dir='E:/03_MarineTraffic/위성연계해경/ais2018_DS_sect'
os.makedirs(path_out_dir,exist_ok=True)
file_list=np.array(recursive_file(path_ais,pattern='*.csv'))

# sect_name='Sokcho2Hosan'
# sect_name='Busan'
# sect_name='Ulsan'
coord=Map.sector()[sect_name]

def extract(DF,coord):
    cond = (coord[0]< DF.lon) & (DF.lon < coord[1]) & (coord[2] < DF.lat) & (DF.lat < coord[3])
    nDF=DF[cond]
    return nDF

for ii in range(len(file_list)):
    # ii=0
    DF=pd.read_csv(file_list[ii])
    DF=extract(DF,coord)
    file_name=file_list[ii].split('\\')[-1][:-4]
    sect_dir=path_out_dir+'/'+sect_name
    os.makedirs(sect_dir,exist_ok=True)
    path_final=sect_dir+'/'+file_name+'_'+sect_name+'.csv'
    print(path_final)
    DF.to_csv(path_final,index=False)