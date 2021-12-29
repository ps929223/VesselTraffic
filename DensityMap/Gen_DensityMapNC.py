import os, sys
path_Lib='D:/programming/SatModel/Lib'
sys.path.append(path_Lib)
import pandas as pd
import numpy as np
from lib_os import *

path_ais='E:/03_MarineTraffic/위성연계해경/ais2018_DS'
file_list=np.array(recursive_file(path_ais,pattern='*.csv'))

tp=pd.read_csv(file_list[0])
minlon, maxlon = np.quantile(tp.lon, [0, 1])
minlat, maxlat = np.quantile(tp.lat, [0, 1])


for ii in range(len(file_list)):
