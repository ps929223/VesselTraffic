import pandas as pd
import numpy as np
import sys
sys.path.append('D:/programming/SatModel/Lib')
from lib_os import *
from tqdm import tqdm


'''
내가 가진 Static AIS 정보 관리
'''

path_DF='E:/03_MarineTraffic/DB/SAIS_DF.csv'
DF=pd.read_csv(path_DF, encoding='cp949')

type_uniq=DF.vessel_type.unique()

## Unknown 정리
intoUnknown=['Unknwon','UNAVAILABLE', 'Not Available']
for ii in range(len(intoUnknown)):
    cond=intoUnknown[ii]==DF.vessel_type
    DF.vessel_type[cond]='Unknown'
DF.vessel_type[DF.vessel_type.isna()]='Unknown'

## intoReserve 정리
intoReserve=['Spare','Reserved']
for ii in range(len(intoReserve)):
    cond=intoReserve[ii]==DF.vessel_type
    DF.vessel_type[cond]='SpareReserved'

## Fishing 정리
DF.vessel_type[DF.vessel_type_code>99]='MaybeFish'

DF.to_csv(path_DF[:-4]+'_r1.csv', index=False)




'''
해경과제 Static AIS 정보 관리
'''
import pandas as pd
import numpy as np
import sys
sys.path.append('D:/programming/SatModel/Lib')
from lib_os import *

path_DF='E:/03_MarineTraffic/DB/CG_AIS_static.csv'
DF=pd.read_csv(path_DF)

type_uniq=DF.typename.unique()


## Multiple 정리
DF.typename[DF.shiptype=='Multiple']='Multiple'
DF.shiptype[DF.shiptype=='Multiple']=np.nan

## Unknown 정리
intoUnknown=['Unknwon','UNAVAILABLE', 'Not Available','Multiple']
for ii in range(len(intoUnknown)):
    cond=intoUnknown[ii]==DF.typename
    DF.typename[cond]='Unknown'
DF.typename[DF.typename.isna()]='Unknown'

## intoReserve 정리
intoReserve=['Spare','Reserved']
for ii in range(len(intoReserve)):
    cond=intoReserve[ii]==DF.typename
    DF.typename[cond]='SpareReserved'

## Fishing 정리
intoFish_cond= ['Fish' in name for name in type_uniq]
intoFish=type_uniq[intoFish_cond]
for ii in range(len(intoFish)):
    cond=intoFish[ii]==DF.typename
    DF.typename[cond]='Fishing'
type_uniq=DF.typename.unique()

DF.typename[DF.typename.isna()]='MaybeFish'
DF.typename[(DF.typename=='Unknown')&(DF.shiptype.astype(float)>99)]='MaybeFish'
DF.typename[(DF.typename=='Unknown')&(DF.mmsi<200000000)]='MaybeFish'
DF.typename[(DF.typename=='Unknown')&(DF.mmsi<413000000)]='MaybeFish'
DF.typename[(DF.typename=='Unknown')&(DF.mmsi>=478000000)]='MaybeFish'
type_uniq=DF.typename.unique()


## Tanker 정리1
intoTanker_cond= ['Tanker' in name for name in type_uniq]
intoTanker=type_uniq[intoTanker_cond]
for ii in range(len(intoTanker)):
    cond=intoTanker[ii]==DF.typename
    DF.typename[cond]='Tanker'
type_uniq=DF.typename.unique()

## DP 정리
intoDP=['FPSO (Floating, Production, Storage, Offloading)',
        'FSO (Floating, Storage, Offloading)',
        'Cable Layer','Drilling Ship','Offshore Support Vessel','Pipe Layer','Platform Supply Ship']
for ii in range(len(intoDP)):
    cond=intoDP[ii]==DF.typename
    DF.typename[cond]='DP'

## Dredge 정리
intoDredge=['Dredger','Dredging','Hopper Dredger']
for ii in range(len(intoDredge)):
    cond=intoDredge[ii]==DF.typename
    DF.typename[cond]='Dredge'

## ForPublic
intoForPublic=['Law Enforcement','Medical Transport',
               'Pollution Control Vessel','Port Tender',
               'Standby Safety Vessel', 'Utility Vessel',
               'Vessel With Anti-Pollution Equipment']
for ii in range(len(intoForPublic)):
    cond=intoForPublic[ii]==DF.typename
    DF.typename[cond]='ForPublic'

## SAR
intoSAR=['Salvage Ship']
for ii in range(len(intoSAR)):
    cond=intoSAR[ii]==DF.typename
    DF.typename[cond]='SAR'

## Special
intoSpecialPurpose=['Crane Ship','Diving','Utility Vessel','WIG']
for ii in range(len(intoSpecialPurpose)):
    cond=intoSpecialPurpose[ii]==DF.typename
    DF.typename[cond]='Special'

## Warship 정리
intoWarship=['Military','Naval/Naval Auxiliary','Patrol Vessel','Ships Not Party to Armed Conflict']
for ii in range(len(intoWarship)):
    cond=intoWarship[ii]==DF.typename
    DF.typename[cond]='Warship'


## Cargo 정리 1
# Cargo, Carrier, Trans Shipment는 포함되지만, Passenger는 포함되지 않아야 함
intoCargo_cond= (np.array(['Cargo' in name for name in type_uniq]) \
                | np.array(['Carrier' in name for name in type_uniq]) \
                | np.array(['Trans Shipment' in name for name in type_uniq])) \
                & np.array(['Passenger' not in name for name in type_uniq])
intoCargo=type_uniq[intoCargo_cond]
for ii in range(len(intoCargo)):
    cond=intoCargo[ii]==DF.typename
    DF.typename[cond]='Cargo'

## Cargo 정리 2
intoCargo = ['Container Ship']
for ii in range(len(intoCargo)):
    cond = intoCargo[ii] == DF.typename
    DF.typename[cond] = 'Cargo'

## Passenger 정리 1
intoPassenger_cond= ['Passenger' in name for name in type_uniq]
intoPassenger=type_uniq[intoPassenger_cond]
for ii in range(len(intoPassenger)):
    cond=intoPassenger[ii]==DF.typename
    DF.typename[cond]='Passenger'

## Passenger 정리 2
intoPassenger = ['Training Ship']
for ii in range(len(intoPassenger)):
    cond = intoPassenger[ii] == DF.typename
    DF.typename[cond] = 'Passenger'

## TugTow 정리
intoTugTow_cond= (np.array(['Tug' in name for name in type_uniq])) \
                 | np.array((['Tow' in name for name in type_uniq]))
intoTugTow=type_uniq[intoTugTow_cond]
for ii in range(len(intoTugTow)):
    cond=intoTugTow[ii]==DF.typename
    DF.typename[cond]='TugTow'

## 길이, 폭 정리
cond=(DF.length==0)&(DF.width==0)
DF.length[cond]=np.nan
DF.width[cond]=np.nan
cond=(DF.length>500)|(DF.width>500)
DF.length[cond]=np.nan
DF.width[cond]=np.nan


DF['typename']=DF['typename'].astype(str)
DF.sort_values(by='mmsi', ascending=True).to_csv(path_DF[:-4]+'_r2.csv', index=False)
count=pd.DataFrame(DF.groupby('typename').count()['mmsi']).rename(columns={'mmsi':'count'})
count.to_csv(path_DF[:-4]+'_count_r2.csv', index=True)
