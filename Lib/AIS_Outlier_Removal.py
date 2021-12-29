'''
-----------------------------------------------
AIS 원자료의 Outlier 제거
- 1) LandMask: 한중일 LM 이미지와 AIS의 밀도맵 이용한 제거
- 2) Gaussian Filter를 이용해 FWHM을 이용해 Sigma를 구하고,
    여러척 선박항적 데이터(dAIS)에서 sigma에 해당하는 Gaussian 분포를 얻은 뒤
    Gaussian 분포와 관측치의 오차한계(Diff)보다 큰 것을 Outlier로 정의하고 제거
개발자: 전호군
초안: 2020.11.06
수정: 2020.01.30 (Land Masking 기능 추가)
개발환경
- Python      3.7.9
- matplotlib  3.1.3
- numpy       1.14.6
- scipy       1.5.2
-----------------------------------------------
'''

''' Define Function '''

def fwhm2sigma(FWHM):
    import numpy as np

    '''
    Get Sigma using FWHM
    '''
    return FWHM / np.sqrt(8 * np.log(2))


def remove_outlier(dAIS, FWHM, Diff):
    '''
    corr_dAIS, outlier_info=remove_outlier(dAIS, FWHM, Diff)
    FWHM을 이용해 Sigma를 구하고,
    여러척 선박항적 데이터(dAIS)에서 sigma에 해당하는 Gaussian 분포를 얻은 뒤
    Gaussian 분포와 관측치의 오차한계(Diff)보다 큰 것을 Outlier로 정의하고 제거
    corr_dAIS: 수정된 AIS
    outelier_info: [[MMSI][Outlier 갯수]]
    '''

    import numpy as np
    from scipy.ndimage import gaussian_filter1d
    import pandas as pd
    import lib.landmask_raster as LM

    # Land Masking
    print('Land Maksing '+str(list(dAIS['ctime'])[-1][:10]))
    dAIS=LM.landmask_raster(dAIS)

    unique_id = np.unique(dAIS.mmsi)
    dAIS=dAIS.sort_values(by=['ctime', 'mmsi'], axis=0)  # descend

    # plt.scatter(dAIS.lon,dAIS.lat,marker='.',s=1)


    print('Outlier Removing: Gaussian Filter')
    outlier_id=[]; outlier_count=[];corr_dAIS=pd.DataFrame([])
    sigma = fwhm2sigma(FWHM)

    for ii in range(len(unique_id)):
        ship_1 = dAIS[unique_id[ii] == dAIS.mmsi] # 선박 1개 항적 추출
        ship_1=ship_1.reset_index()
        smoo_x = gaussian_filter1d(ship_1.lon, sigma) # Gaussian Smoothing
        smoo_y = gaussian_filter1d(ship_1.lat, sigma)
        dlon_smoo = abs(ship_1.lon - smoo_x) # 오차계산
        dlat_smoo = abs(ship_1.lat - smoo_y)
        outlier_condition = (dlon_smoo > Diff) | (dlat_smoo > Diff) # Outlier 색출
        if sum(outlier_condition)>0:
            outlier_id.append(ship_1.mmsi[0]) # Outlier가 1개 이상인 경우, ID 저장
            outlier_count.append(sum(outlier_condition))
        tp=ship_1[~outlier_condition] # 선박 1척의 Outlier를 제거한 항적데이터 생성
        corr_dAIS=pd.concat([corr_dAIS, tp],axis=0) # 선박 여러척의 Outlier 제거데이터 생성
    outlier_info=[outlier_id,outlier_count]
    corr_dAIS=corr_dAIS.reset_index()

    try:
        corr_dAIS=corr_dAIS.drop(columns=['level_0','index'])
    except:
        print('No level_0 or index')
    return corr_dAIS, outlier_info

def plot_everyship(dAIS):
    import matplotlib.pyplot as plt
    import numpy as np

    plt.figure()
    unique_id = np.unique(dAIS.mmsi)
    for ii in range(len(unique_id)):
        ship_1 = dAIS[unique_id[ii] == dAIS.mmsi]  # 선박 1개 항적 추출
        plt.plot(ship_1.lon,ship_1.lat)

def plot_IDs_ship(dAIS, IDs):
    # list에 지정된 ID만 출력
    import matplotlib.pyplot as plt
    plt.figure()
    for ii in range(len(IDs)):
        tp=dAIS[IDs[ii]==dAIS.mmsi]
        plt.plot(tp.lon,tp.lat)

#
# #
# # ''' Test Code in this Script '''
# #
# import pandas as pd
#
# ## Input file
# dAIS=pd.read_csv('AIS/csv/Busan_dAIS_Outlier_Before.csv')
# dAIS=pd.read_csv('AIS/csv/dAIS_20200205000000_20200205235959.csv')
# dAIS=pd.read_csv('E:\해상교통정보\T-AIS\Busan\Out_Rem\dAIS_20191007000000_20191007235959_OutRem.csv')
# dAIS=pd.read_csv('E:\해상교통정보\T-AIS\Busan\dAIS_20200206000000_20200206235959.csv')
# input_dAIS = 'AIS/csv/dAIS_20200206000000_20200206235959.csv'


# import matplotlib.pyplot as plt
# import matplotlib.patches as patches
# plt.scatter(dAIS.lon, dAIS.lat)
# plt.plot(res[0],res[1])
# out_AIS_dir='AIS/csv/Busan_dAIS_Outlier_After.csv'
#
# ## Parameter
# FWHM=5
# Diff=0.1
#
# ## 모든선박 전후
# corr_dAIS, outlier_info=remove_outlier(dAIS,FWHM,0.03) # 쾌속선 40kt를 제외한 다른 선박이 3분이내 이동할 수 없는 범위 0.03 deg
# plot_everyship(dAIS)
# plot_everyship(corr_dAIS)
#
# ## 원하는 선박만 전후
# IDs=outlier_info[0] # outlier정보 중 ID만 추출
# plot_IDs_ship(dAIS, IDs)
# plot_IDs_ship(corr_dAIS, IDs)

#
# # Output file
# corr_dAIS.to_csv(out_AIS_dir)
#
#
# ''' Python Library Version Check '''
# import matplotlib
# import numpy as np
# import scipy
#
# print(matplotlib.__version__)
# print(np.__version__)
# print(scipy.__version__)



# ''' Test Code in other script '''
# import AIS.AIS_Outlier_Removal as AOR
# import pandas as pd
# 생성한 python 함수를 불러오려면, 해당 subfolder내에 비어있는 __init__.py 생성 먼저 할 것

#
# # Input file
# dAIS=pd.read_csv('AIS/csv/Busan_dAIS_Outlier_Before.csv')
# out_AIS_dir='AIS/csv/Busan_dAIS_Outlier_After.csv'
#
# # Parameter
# FWHM=5
# Diff=0.03
#
# corr_dAIS, outlier_info=AOR.remove_outlier(dAIS,FWHM,Diff) # 쾌속선 40kt를 제외한 다른 선박이 3분이내 이동할 수 없는 범위 0.03 deg
# AOR.plot_everyship(dAIS)
# AOR.plot_everyship(corr_dAIS)
