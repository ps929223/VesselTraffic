'''
Json으 DataFrame으로 변환하는 코드
2021.12.14
전호군
'''

def Json2DF(path_json):
    '''
    path_json: JSON 파일 경로
    '''
    import json
    import pandas as pd
    with open(path_json) as json_file:
        json_data = json.load(json_file)
    DF=pd.DataFrame(json_data)
    return DF

''' Test Code '''
path_json= 'ais.json'
DF=Json2DF(path_json)

path_ocean='oceanWeather_00.json'
DF=Json2DF(path_ocean)