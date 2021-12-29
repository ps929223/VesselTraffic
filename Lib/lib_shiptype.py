
def find_shiptype(mmsi,static,typesort):
    import Lib.lib_colors as cls

    tab_color = cls.tab_color()

    # mmsi=mmsis[ii]
    # mmsi=431000234
    cond_idx=mmsi==static.mmsi
    if sum(cond_idx)==1:
        try:
            typenum=static.shiptype[cond_idx].astype(float)
            cond_typeidx=int(typenum)==typesort.Type_Code
            if sum(cond_typeidx)==1:
                typename=list(typesort.This_Research[cond_typeidx])[0]
                cond_color=typename==typenames
                chosen_color=tab_color[int(np.where(cond_color)[0])]
            else:
                typename = 'unknown'
                chosen_color = tab_color[7]
        except:
            typename = 'unknown'
            chosen_color = tab_color[7]
    else:
        typename='unknown'
        chosen_color=tab_color[7]
    return typename, chosen_color

