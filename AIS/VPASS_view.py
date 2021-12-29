import pandas as pd
import numpy as np
import sys
sys.path.append('D:/programming/SatModel/Lib')
from lib_os import *

path_dir='E:/03_MarineTraffic/위성연계해경/vpass2018'
file_list=np.array(recursive_file(path_dir,'*.csv'))
vars=['id','kst','lon', 'lat','sog','cog','hdg','battery','a2','harborIn','gearType','a5','a6','a7','baseStation_id','a9']

DF=pd.read_csv(file_list[0])
DF.columns=vars
DF.lon=DF.lon/600000
DF.lat=DF.lat/600000

print(min(DF.a5), max(DF.a5))
print(min(DF.a6), max(DF.a6))
print(min(DF.a9), max(DF.a9))
