'''
--------------------------------------------
Geometry 함수모음
작성자: 전호군
최근업뎃: 2021.12.12
---------------------------------------------
'''


def gyro2deg(gyro):
    '자이로 방위를 평면방위로 변환'
    # 예) 본선컴파스 방위 90도 = 평면방위 0
    deg = -gyro + 90
    if deg < 360:
        deg = (deg + 360) % 360
    elif deg > 360:
        deg = deg % 360
    if deg == 360:
        deg = 0
    return deg

def deg2gyro(deg):
    '평면방위를 Gyro방위로 변환'
    gyro=-deg+90+360%360
    return gyro

def get_brng(lon1, lon2, lat1, lat2):
    import numpy as np
    dLon = (lon2 - lon1)
    y = np.sin(dLon) * np.cos(lat2)
    x = np.cos(lat1) * np.sin(lat2) - np.sin(lat1) * np.cos(lat2) * np.cos(dLon)
    brng = np.arctan2(y, x)
    brng = -np.rad2deg(brng)
    brng[brng < 0]=brng[brng < 0]+360
    return brng



def dist_harversine(lon1, lon2,lat1,lat2):
    # 두개의 경위도정보로 거리[km] 계산
    import numpy as np

    R = 6378137.0  # [m] Earth Radius 지구반지름
    lon1 = np.radians(lon1)
    lat1 = np.radians(lat1)
    lon2 = np.radians(lon2)
    lat2 = np.radians(lat2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    # Haversine Formula
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    dist = R * c  # [m]

    return dist

def date_diff_in_Seconds(dt2, dt1):
    from datetime import datetime, time
    timedelta = dt2 - dt1
    return timedelta.days * 24 * 3600 + timedelta.seconds


def spherical_distance(lon1, lat1, lon2, lat2):
    from scipy import sin, cos, tan, arctan, arctan2, arccos, pi

    phi1 = 0.5 * pi - lat1
    phi2 = 0.5 * pi - lat2
    r = 0.5 * (6378137 + 6356752)  # mean radius in meters
    t = sin(phi1) * sin(phi2) * cos(lon1 - lon2) + cos(phi1) * cos(phi2)
    return r * arccos(t)


def ellipsoidal_distance(lon1, lat1, lon2, lat2):
    from scipy import sin, cos, tan, arctan, arctan2, arccos, pi

    a = 6378137.0  # equatorial radius in meters
    f = 1 / 298.257223563  # ellipsoid flattening
    b = (1 - f) * a
    tolerance = 1e-11  # to stop iteration

    phi1, phi2 = lat1, lat2
    U1 = arctan((1 - f) * tan(phi1))
    U2 = arctan((1 - f) * tan(phi2))
    L1, L2 = lon1, lon2
    L = L2 - L1

    lambda_old = L + 0

    while True:

        t = (cos(U2) * sin(lambda_old)) ** 2
        t += (cos(U1) * sin(U2) - sin(U1) * cos(U2) * cos(lambda_old)) ** 2
        sin_sigma = t ** 0.5
        cos_sigma = sin(U1) * sin(U2) + cos(U1) * cos(U2) * cos(lambda_old)
        sigma = arctan2(sin_sigma, cos_sigma)

        sin_alpha = cos(U1) * cos(U2) * sin(lambda_old) / sin_sigma
        cos_sq_alpha = 1 - sin_alpha ** 2
        cos_2sigma_m = cos_sigma - 2 * sin(U1) * sin(U2) / cos_sq_alpha
        C = f * cos_sq_alpha * (4 + f * (4 - 3 * cos_sq_alpha)) / 16

        t = sigma + C * sin_sigma * (cos_2sigma_m + C * cos_sigma * (-1 + 2 * cos_2sigma_m ** 2))
        lambda_new = L + (1 - C) * f * sin_alpha * t
        if abs(lambda_new - lambda_old) <= tolerance:
            break
        else:
            lambda_old = lambda_new

    u2 = cos_sq_alpha * ((a ** 2 - b ** 2) / b ** 2)
    A = 1 + (u2 / 16384) * (4096 + u2 * (-768 + u2 * (320 - 175 * u2)))
    B = (u2 / 1024) * (256 + u2 * (-128 + u2 * (74 - 47 * u2)))
    t = cos_2sigma_m + 0.25 * B * (cos_sigma * (-1 + 2 * cos_2sigma_m ** 2))
    t -= (B / 6) * cos_2sigma_m * (-3 + 4 * sin_sigma ** 2) * (-3 + 4 * cos_2sigma_m ** 2)
    delta_sigma = B * sin_sigma * t
    s = b * A * (sigma - delta_sigma)

    return s

def m2deg(meter,lat1, heading):

    import numpy as np
    import pandas as pd
    import pyproj

    # meter=200
    # lat1=45 # AIS의 GPS 위도
    # heading=90

    # 거리,방위 계산을 위한 함수
    geod = pyproj.Geod(ellps='WGS84')
    lat=np.arange(0,90.01,.01)
    lon=[0, 1]
    lat_dist=[]
    lon_dist=[]

    for ii in range(0,len(lat)-1):
        lat_dist.append(geod.inv(lon[0], lat[ii], lon[0], lat[ii+1])[2]) # 위도1도에 대한 거리 m
        lon_dist.append(geod.inv(lon[0], lat[ii], lon[1], lat[ii])[2]) # 경도1도에 대한 거리 m

    idx=int(np.where(abs(lat-lat1)==min(abs(lat-lat1)))[0]) # 내 위치에 해당하는 거리 idx
    my_x_coff=1/lon_dist[idx] # 내 위치의 거리 1m를 deg로 변환하는 계수
    my_y_coff=1/lat_dist[idx]

    brg=(360-heading+90)%360

    meter=np.array(meter)
    deg_x=meter*my_x_coff*np.cos(heading*np.pi/180)
    deg_y=meter*my_y_coff*np.sin(heading*np.pi/180)
    deg=[deg_x,deg_y]

    return deg

# ''' test code '''
# lat1=[]
# heading=90
# meter=91286
# deg=m2deg(meter, lat1, heading)
# print(deg)

lon=129
lat=35
heading=90

def draw_ship(dims,lon,lat,heading):

    brg=(360-heading+90)%360

    ### Azimuth 방위(진북 000)를 좌표평면 방위(진북 090)로 변환
    front_deg=brg
    back_deg=brg+180
    left_deg=brg+90
    right_deg=brg-90

    delta=[[]]*4
    ### 선수, 선미, 좌현끝, 우현끝 좌표구하기
    dfront=m2deg(dims[0],lat,front_deg)
    dback=m2deg(dims[1],lat,back_deg)
    dleft=m2deg(dims[2],lat,left_deg)
    dright=m2deg(dims[3],lat,right_deg)

    xs=lon+np.array([dfront[0], dback[0],dleft[0],dright[0]])
    ys=lat+np.array([dfront[1], dback[1],dleft[1],dright[1]])


    # 좌우현의 중간 위치
    c_x_lr=np.mean([xs[2],xs[3]])
    c_y_lr=np.mean([ys[2],ys[3]])

    # 좌우현 중간위치에서 선수방향으로 이동할 거리
    d_move=(dimA+dimB)/2-dimB

    # 보정중심위치
    c_lon,c_lat=getxy(c_x_lr,c_y_lr,d_move,front_deg)

    ### 선박모양 그리기 5각형
    F_x = c_x_lr + m2deg(dims[0],c_lat) * np.cosd(front_deg)
    F_y = c_y_lr + m2deg(dims[0],c_lat) * np.sind(front_deg)
    FL_x = left_x + m2deg(dimA-np.mean([dims[2],dims[3]]),dleft[1]) * np.cosd(front_deg)
    FL_y = left_y + m2deg(dimA-np.mean([dims[2],dims[3]]),dleft[1]) * np.sind(front_deg)
    FR_x = right_x + m2deg(dimA-np.mean([dims[2],dims[3]]),dright[1]) * np.cosd(front_deg)
    FR_y = right_y + m2deg(dimA-np.mean([dims[2],dims[3]]),dright[1]) * np.sind(front_deg)
    BL_x = left_x + m2deg(dims[1],dback[1]) * np.cosd(front_deg+180)
    BL_y = left_y + m2deg(dims[1],dback[1]) * np.sind(front_deg+180)
    BR_x = right_x + m2deg(dims[1],dback[1]) * np.cosd(front_deg+180)
    BR_y = right_y + m2deg(dims[1],dback[1]) * np.sind(front_deg+180)








#
#
#
# dims=[100, 30, 20, 20] # ABCD
# lat=35
# meter2deg(dims,35,51)
#
# meter2deg(meter,)
#
# # ''' test code '''
# lons=[[129.33511352539062,  129.334625,129.335663,129.336456,129.335892,129.334854]]
# lats=[[35.20186996459961, 35.20276,35.2024345,35.20276,35.2022, 35.2015152]]
#
#
#
#
#
# # 부산인근 10.55km
# coord1=[129.1486901576661, 35.11015548424928]
# coord2=[129.2511901904047, 35.15452079858077]
# #
# # 인도네시아 1176km
# coord1=[130.5517887818125,5.1274017938426]
# coord2=[140.0809898612052,0.5031802717845857]
#
#
# lon1=coord1[0]
# lon2=coord2[0]
# lat1=coord1[1]
# lat2=coord2[1]
#
#
# dist_harversine(lon1, lat1,lon2, lat2)
# ellipsoidal_distance(lon1, lat1,lon2, lat2)
#
#
#
# lats=np.arange(0,90,1)
# harversine_dist=[]
# ellipsoidal_dist=[]
# Geod_dist=[]
# for ii in range(len(lats)-1):
#     harversine_dist.append(dist_harversine(lon1, lats[ii],lon2, lats[ii+1]))
#     ellipsoidal_dist.append(ellipsoidal_distance(lon1, lats[ii],lon2, lats[ii+1]))
#     azi1,azi2,dist=geod.inv(lon1, lats[ii],lon2, lats[ii+1])
#     Geod_dist.append(dist)
#
# harversine_dist=np.array(harversine_dist)
# ellipsoidal_dist=np.array(ellipsoidal_dist)
# Geod_dist=np.array(Geod_dist)
#
#
# data=pd.DataFrame([[lon1]*(len(lats)-1),lats[:-1],[lon2]*(len(lats)-1),lats[1:],harversine_dist,ellipsoidal_dist,Geod_dist])
# data=data.T
# data.columns=['lon1','lat1','lon2','lat2','haversine','ellipsoidal','Geod']