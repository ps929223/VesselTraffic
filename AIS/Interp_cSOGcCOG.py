
import os, sys
sys.path.append('D:/programming/SatModel/Lib')
from lib_os import *
import pandas as pd
import numpy as np
import Lib.lib_AIS_Intp_cSOGcCOG as AIC
# sect_name='Ulsan'
sect_name='Sokcho2Hosan'
# sect_name='Busan'

path_ais='E:/03_MarineTraffic/위성연계해경/ais2018_DS_sect/'+sect_name
path_out_dir='E:/03_MarineTraffic/위성연계해경/ais2018_DS_sect_intp/'+sect_name
os.makedirs(path_out_dir,exist_ok=True)
file_list=np.array(recursive_file(path_ais,pattern='*'+sect_name+'.csv'))

for ii in range(len(file_list)):
    # ii=0
    DF=pd.read_csv(file_list[ii])
    DF=AIC.intp_compute(DF=DF,LT=0,minute=5)
    file_name=file_list[ii].split('\\')[-1][:-4]
    path_save_in=path_out_dir+'/'+sect_name
    os.makedirs(path_save_in, exist_ok=True)
    path_final=path_save_in+'/'+file_name+'_intp.csv'
    print(path_final)
    DF.to_csv(path_final, index=False)


