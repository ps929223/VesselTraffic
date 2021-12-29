'''
--------------------------------------------
T-AIS 원자료를 원자료를 전처리
작성자: 전호군
수정: 2021.12.12 @ 전체코드 수정

개발환경
- Python      3.7.9
- matplotlib  3.1.3
- numpy       1.14.6
---------------------------------------------
'''


def intp_compute(DF,LT=0,minute=5):
    '''
    new_dAIS=intp_compute(dAIS,LT,minute)
    DF: DataFrame
    LT: int # Zone Hour KST=+9
    minute: Interpolation interval
    '''
    print('Interpolation & Computing cSOG, cCOG')
    import numpy as np
    import Lib.lib_geometry as geo
    import pandas as pd
    import pyproj

    # DF=pd.read_csv('E:/03_MarineTraffic/위성연계해경/ais2018_DS_sect\\Busan\\Dynamic_20180111_DS_Busan.csv')


    # 거리,방위 계산을 위한 함수
    geod = pyproj.Geod(ellps='WGS84')

    ## AIS 정렬
    DF = DF.sort_values(by=['kst', 'mmsi'])
    ## COG, SOG 보간을 위한 radian 변환
    DF['cog']=np.deg2rad(DF['cog'])
    DF['hdg']=np.deg2rad(DF['hdg'])

    unique_id= np.unique(DF['mmsi'])

    Merged_DF=pd.DataFrame([])
    # ii=0
    for ii in range(len(unique_id)): # mmsi 순서대로 진행
        # print(round(ii/len(unique_id)*100,3))
        ship_1=DF[DF['mmsi']==unique_id[ii]]
        #         ship_1=ship_1.reset_index()
        #         # 선박 1척의 COG, SOG 계산
        ship_1_typename = list(ship_1.typename.unique())[0]

        if len(ship_1) == 1:
            cCOG = ship_1['cog'][ship_1.index[0]] # 데이터가 1개면 있는값 그대로 1개만 반영
            cSOG = ship_1['sog'][ship_1.index[0]]
        else:
            ## time columns 의 포맷변경: 1차적인 1분 보간 위함
            ship_1['kst'] = pd.to_datetime(ship_1['kst'])
            ## time을 Index로 설정: 1차적인 1분 보간 위함
            ship_1=ship_1.set_index('kst')
            # 5분 리샘플링 전, 촘촘한 자료 확보를 위한 1분 보간
            # i, i-1 의 시간차가 1초 이하인 경우, 속도가 비정상적으로 계산됨
            # 이 작업을 거쳐야 cCOG, cSOG 계산에 오류가 발생하지 않음
            ship_1 = ship_1.resample('1T').median()  # resample 1min
            ship_1 = ship_1.interpolate(method='time')

            # Index 재설정: 기존 time이 Index된 것을 풀어야, delta time(dtime) 계산할 수 있음
            ship_1 = ship_1.reset_index()

            # delta 계산
            kst1 = ship_1['kst'][:-1]
            kst2 = np.array(ship_1['kst'][1:])
            dtime = []
            for jj in range(len(kst1)):
                dtime.append(geo.date_diff_in_Seconds(kst2[jj], kst1[jj]) / (60 * 60))  # 초단위를 시간단위로 변경

            # cCOG, cSOG 계산위한 경위도 추출
            lon1 = np.array(ship_1['lon'][:-1])
            lon2 = np.array(ship_1['lon'][1:])
            lat1 = np.array(ship_1['lat'][:-1])
            lat2 = np.array(ship_1['lat'][1:])


            # cCOG 계산
            cCOG=[ship_1['cog'][0]]+list(np.remainder(360+geod.inv(lon1,lat1,lon2,lat2)[0],360)) # azi_forward,azi_backward,dist[unit: m]

            # cSOG 계산
            tp_dist=np.array(geod.inv(lon1,lat1,lon2,lat2)[2]) # [km]
            cSOG=[ship_1['sog'][0]]+list(tp_dist/1852/np.array(dtime)) #

        # 계산된 선속을 ship_1에 새로운 행에 추가
        ship_1['cSOG']=cSOG
        ship_1['cCOG']=cCOG

        # 5분 보간
        ship_1['kst'] = pd.to_datetime(ship_1['kst'])
        ship_1 = ship_1.set_index('kst')
        ship_1 = ship_1.resample(str(minute)+'T').median()  # resample
        ship_1['typename']=ship_1_typename

        # # land Masking: 5분 보간자료여야 시간이 5배 단축됨
        # ship_1 = IP.inpolygon(ship_1)
        #
        # # land Masking으로 지운 부분 다시 보간
        # if len(ship_1)>1:
        #     ship_1.ctime = pd.to_datetime(ship_1.ctime)
        #     ship_1 = ship_1.set_index('ctime')
        #     ship_1 = ship_1.resample(str(minute) + 'T').median()  # resample
        # LT=0
        # ship_1을 켜켜히 쌓음
        Merged_DF=pd.concat([Merged_DF, ship_1], axis=0)

    # 처음에 radian으로 변경한 것을 deg로 다시 바꿈
    Merged_DF['cog'] = np.rad2deg(Merged_DF['cog'])
    Merged_DF['hdg'] = np.rad2deg(Merged_DF['hdg'])
    Merged_DF=Merged_DF.reset_index()
    Merged_DF['kst']=pd.to_datetime(Merged_DF['kst'])+pd.DateOffset(hours=LT, minutes=0)

    try:
        Merged_DF=Merged_DF.drop(columns='index')
        Merged_DF = Merged_DF[['kst', 'mmsi', 'lat', 'lon', 'sog', 'cog',\
                             'cSOG', 'cCOG', 'hdg', 'length', 'width','typename']]
    except:
        print("No additive index column")

    return Merged_DF