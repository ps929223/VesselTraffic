import os, sys
import numpy as np
import pandas as pd

sys.path.append('D:/programming/SatModel/Lib')
from lib_os import *
import Map as Map
import matplotlib.pyplot as plt
import Lib.lib_tab as tab
from tqdm import tqdm

tab_colors=tab.tab_color()


path_dir='E:/03_MarineTraffic/위성연계해경/ais2018_DS_sect'
path_out_dir='E:/20_Product/MarineTraffic/AIS/TypeLine'

sect_name='Ulsan'
coord=Map.sector()[sect_name]
path_out_subdir=path_out_dir+'/'+sect_name
os.makedirs(path_out_subdir, exist_ok=True)

file_list=np.array(recursive_file(path_dir,'*_'+sect_name+'.csv'))

plt.figure(4, figsize=(17,15))

for ii in range(len(file_list)):
    # ii=0
    DF=pd.read_csv(file_list[ii])
    unique_type=list(DF.groupby('typename').count().sort_values(by='mmsi', ascending=False).index) # 내림차순으로 정리
    # 내림차순 정리해야 나중에 색깔 배정이 좋음
    unique_mmsi=DF['mmsi'].unique()

    m = Map.making_map(coord, map_res='f', grid_res=0.05)
    xx, yy = m(DF.lon, DF.lat)
    for jj in range(len(unique_mmsi)):
        # jj=0
        cond_mmsi=unique_mmsi[jj]==DF['mmsi']
        new_DF=DF[cond_mmsi]
        new_DF_type=new_DF['typename'].unique()
        type_num=int(np.where(new_DF_type==unique_type)[0])
        type_color=tab_colors[type_num]
        m.plot(xx[cond_mmsi],yy[cond_mmsi],c=type_color, linewidth='.5', label=list(new_DF_type)[0])
    ### 중복되는 legend 지워서 표시
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys(), bbox_to_anchor=(1.04,1), loc="upper left")

    ## 제목표시
    date_str=file_list[ii].split('\\')[-1].split('_')[1]
    title='TAIS '+date_str
    plt.title(title)

    plt.tight_layout()
    path_final=path_out_subdir+'/TypeLine_'+date_str+'.png'
    print(path_final)
    plt.savefig(path_final)
    plt.clf()