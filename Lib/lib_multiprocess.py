
def pararlled_df(df,func,n_cores):
    '''
    https://jonsyou.tistory.com/27
    :param df:
    :param func:
    :param n_cores:
    :return:
    '''
    import multiprocessing as mp
    import numpy as np
    import pandas as pd
    ### 병렬처리 가능한 CPU는 몇개?
    # n_cores = mp.cpu_count()

    df_split=np.array_split(df,n_cores)
    pool=mp.Pool(n_cores)
    df=pd.concat(pool.map(func,df_split))
    pool.close()
    pool.join()
    return df
