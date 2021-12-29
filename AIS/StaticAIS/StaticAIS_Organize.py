'''
AIS static match
2021.12.02
'''

import pandas as pd
import numpy as np
import sys
sys.path.append('D:/programming/SatModel/Lib')
from lib_os import *
from tqdm import tqdm

path_sais='D:/프로그래밍/KIO_FW/AIS/csv/sAIS_all.csv'
path_dais_dir='E:/03_MarineTraffic/위성연계해경/ais2018'


'''
2018년 AIS 동적데이터에서 MMSI만 추출
'''

file_list=np.array(recursive_file(path_dais_dir,'*.csv'))

MMSIs=[]
for ii in range(len(file_list)):
    # ii=0
    print(file_list[ii])
    tp=pd.read_csv(file_list[ii], skiprows=2, encoding='cp949')
    MMSIs=MMSIs+list(tp['MMSI'].unique())

MMSIs=np.unique(MMSIs)


vars=['mmsi', 'imo', 'name', 'shiptype','typename','length','width','flag', 'a','b','c','d']
DF=np.zeros((len(MMSIs),len(vars)))
DF[:]=np.nan
DF=pd.DataFrame(DF,columns=vars)


sAIS=pd.read_csv(path_sais)

for ii in tqdm(range(len(MMSIs))):
    DF.mmsi[ii]=MMSIs[ii]
    cond_idx=MMSIs[ii]==sAIS.mmsi
    if sum(cond_idx)==0:
        continue
    elif sum(cond_idx)==1:
        DF.imo[ii] = list(sAIS.imonumber[cond_idx])[0]
        DF.name[ii] = list(sAIS.name[cond_idx])[0]
        DF.shiptype[ii] = list(sAIS.shiptype[cond_idx])[0]
        DF.a[ii] = list(sAIS.a[cond_idx])[0]
        DF.b[ii] = list(sAIS.b[cond_idx])[0]
        DF.c[ii] = list(sAIS.c[cond_idx])[0]
        DF.d[ii] = list(sAIS.d[cond_idx])[0]
    elif sum(cond_idx)>1:
        DF.imo[ii] = list(sAIS.imonumber[cond_idx])[0]
        DF.name[ii] = list(sAIS.name[cond_idx])[0]
        DF.shiptype[ii] = 'Multiple'
        DF.a[ii] = list(sAIS.a[cond_idx])[0]
        DF.b[ii] = list(sAIS.b[cond_idx])[0]
        DF.c[ii] = list(sAIS.c[cond_idx])[0]
        DF.d[ii] = list(sAIS.d[cond_idx])[0]

DF.to_csv('E:/AIS_static.csv', index=False)
print(sum(np.isnan(DF.imo))/len(DF)) # 미수집항목 ??? / 106443 # 0.88

'''
Lloyd  DB에서 정적정보 추출
'''
import pandas as pd
import numpy as np
path_AISstatic='E:/AIS_static.csv'
path_lloyd='E:/03_MarineTraffic/Lloyd/ShipData.csv'
DF=pd.read_csv(path_AISstatic, encoding='cp949')
lloyd=pd.read_csv(path_lloyd, encoding='cp949')
DF['typename']=np.nan
DF['length']=np.nan
DF['width']=np.nan
DF['flag']=np.nan
for ii in tqdm(range(len(DF))):
    # ii=0
    cond_idx=DF.mmsi[ii]==lloyd.MaritimeMobileServiceIdentityMMSINumber
    if sum(cond_idx)==0:
        continue
    else:
        DF.imo[ii] = list(lloyd.LRIMOShipNo[cond_idx])[0]
        DF.name[ii] = list(lloyd.ShipName[cond_idx])[0]
        DF.typename[ii]=list(lloyd.ShiptypeLevel4[cond_idx])[0]
        DF.length[ii] = list(lloyd.LengthOverallLOA[cond_idx])[0]
        DF.width[ii] = list(lloyd.Breadth[cond_idx])[0]
        DF.flag[ii] = list(lloyd.FlagName[cond_idx])[0]
print(sum(np.isnan(DF.imo))/len(DF)) # 미수집항목 95166 / 106443 # 0.80
DF.to_csv('E:/AIS_static.csv', index=False)

'''
S-AIS의 정적정보 집합
'''
path_SAIS_dir='E:/03_MarineTraffic/CSV'
file_list=np.array(recursive_file(path_SAIS_dir,'*.csv'))
SAIS_DF=pd.DataFrame()
for ii in range(len(file_list)):
    # ii=0
    print(file_list[ii])
    tp=pd.read_csv(file_list[ii])
    SAIS_DF=pd.concat([SAIS_DF, tp], axis=0)
    SAIS_DF = SAIS_DF[~SAIS_DF['mmsi'].duplicated()]  # 중복 mmsi 제거
SAIS_DF.to_csv('E:/03_MarineTraffic\Lloyd/SAIS_DF.csv', index=False)/



'''
SAIS에서 정적정보 추출
'''

import pandas as pd
import numpy as np
from tqdm import tqdm

path_AISstatic='E:/AIS_static.csv'
path_SAIS='E:/03_MarineTraffic\Lloyd/SAIS_DF.csv'
DF=pd.read_csv(path_AISstatic, encoding='cp949')
SAIS_DF=pd.read_csv(path_SAIS, encoding='cp949')

for ii in tqdm(range(len(DF))):
    # ii=0
    cond_idx=DF.mmsi[ii]==SAIS_DF.mmsi
    if sum(cond_idx)==0:
        continue
    else:
        if not np.isnan(list(SAIS_DF.imo[cond_idx])[0]):
            DF.imo[ii] = list(SAIS_DF.imo[cond_idx])[0]
        if not list(SAIS_DF.vessel_name[cond_idx])[0]=='nan':
            DF.name[ii] = list(SAIS_DF.vessel_name[cond_idx])[0]
        if not list(SAIS_DF.vessel_type_code[cond_idx])[0]=='nan':
            DF.shiptype[ii]=list(SAIS_DF.vessel_type_code[cond_idx])[0]
        if not list(SAIS_DF.vessel_type[cond_idx])[0]=='nan':
            DF.typename[ii]=list(SAIS_DF.vessel_type[cond_idx])[0]
        if not np.isnan(list(SAIS_DF.length[cond_idx])[0]):
            DF.length[ii] = list(SAIS_DF.length[cond_idx])[0]
        if not np.isnan(list(SAIS_DF.width[cond_idx])[0]):
            DF.width[ii] = list(SAIS_DF.width[cond_idx])[0]
        if not list(SAIS_DF.flag[cond_idx])[0]=='nan':
            DF.flag[ii] = list(SAIS_DF.flag[cond_idx])[0]
print(sum(np.isnan(DF.imo))/len(DF)) # 미수집항목 95166 / 106443 # 0.80
DF.to_csv('E:/AIS_static.csv', index=False)

