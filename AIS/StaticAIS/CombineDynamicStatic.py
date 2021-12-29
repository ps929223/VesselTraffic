import pandas as pd
import numpy as np
import sys, os
sys.path.append('D:/programming/SatModel/Lib')
from lib_os import *
from tqdm import tqdm

path_sais='E:/03_MarineTraffic/DB/CG_AIS_static_r2.csv'
path_dais_dir='E:/03_MarineTraffic/위성연계해경/ais2018'
path_ais_out='E:/03_MarineTraffic/위성연계해경/ais2018_DS'
os.makedirs(path_ais_out,exist_ok=True)

file_list=np.array(recursive_file(path_dais_dir, 'Dynamic*.csv'))
vars=['mmsi', 'kst', 'lat', 'lon', 'sog','cog','hdg']
sais=pd.read_csv(path_sais)[['mmsi','typename','length','width']]

for ii in range(len(file_list)):
    # ii=0
    file_name=file_list[ii].split('\\')[-1]
    print(file_name)
    tp=pd.read_csv(file_list[ii], skiprows=2, encoding='cp949')
    tp.columns=vars
    tp2=tp.join(sais.set_index('mmsi'), on='mmsi')
    tp2.to_csv(path_ais_out+'/'+file_name[:-4]+'_DS.csv', index=False)






