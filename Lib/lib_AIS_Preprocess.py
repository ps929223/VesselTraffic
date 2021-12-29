'''
--------------------------------------------
AIS 전처리 main
개발자: 전호군
초안: 2021.01.03

개발환경
- Python      3.7.9
- numpy       1.14.6
- pandas
---------------------------------------------
'''


def pre_process(input_dAIS,Area,FWHM=5,Diff=0.03,LT=9,minute=5):
    '''
    newdAIS=pre_process(input_dAIS,FWHM,Diff,LT,minute)
    input_dAIS='AIS/csv/dAIS_20200206000000_20200206235959.csv'
    FWHM= 5
    Diff=0.03
    LT=9
    minute=5
    '''

    import pandas as pd
    import lib.AIS_Make_DF as AMD
    import lib.AIS_Outlier_Removal as AOR
    import lib.landmask_raster as LM


    print('Preprocessing AIS')
    print(input_dAIS.split('/')[2])

    '1. Land Mask 와 Gaussian Filter 기반 Outlier 제거'
    # Outlier 제거 후 저장
    dAIS=pd.read_csv(input_dAIS)
    dAIS,outlier_info=AOR.remove_outlier(dAIS,FWHM,Diff)
    if len(dAIS)>2:
        dAIS.to_csv('E:/해상교통정보/T-AIS/'+Area+'/Out_Rem/'+input_dAIS.split('/')[-1][:-4]+'_OutRem.csv')

        '2. cSOG, cCOG 계산 & 시간보간'
        # 입력파일 Outlier 제거
        dAIS=AMD.intp_compute(dAIS,LT,minute)

        # '2-1. 보간 후 생겼을 육지 위 자료 LM'
        # dAIS=LM.landmask_raster(dAIS)
        # print('Complete 2nd LM')

        '3. length정보 반영'
        sAIS=AMD.download_sAIS()
        # input_sAIS='AIS/csv/sAIS_all.csv'
        # sAIS=pd.read_csv(input_sAIS)
        # 입력파일 dAIS, sAIS
        dAIS=AMD.get_type_length(dAIS,sAIS)
        file_name=input_dAIS.split('/')[4][:-4]
        if len(dAIS) > 2:
            dAIS.to_csv('E:/해상교통정보/T-AIS/'+Area+'/processed/'+file_name+'_processed.csv', index=False)


    return dAIS


' Test Code '

## Outlier 제거 후 저장
# 입력파일 원본

#
## Outlier 제거 후 저장
# 입력파일 원본
# input_dAIS='E:/해상교통정보/T-AIS/Busan/dAIS_20200205000000_20200205235959.csv'
#
# pre_process(input_dAIS,Area='Busan',FWHM=5,Diff=0.03,LT=9,minute=5)