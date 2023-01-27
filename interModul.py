'''Модуль двойно интерполяции'''
'''Функция нахождения индексов смежных колонок с искомым значением'''
def index_search(t1, x):
    for i in range(len(t1)):
        if t1[0] < t1[-1]:
            if x > t1[i]: continue
            else: break
        if t1[0] > t1[-1]:
            if x < t1[i]: continue
            else: break
    return i, abs(i-1)

def interpoi(t1, t2, yy, lineEditEnd):
    print("-------------------------------------")
    # lineEditEnd.setStyleSheet("background-color: rgb(220, 220, 220);")
    i = index_search (t1, yy)
    a1 = t1[i[0]]; a2 = t1[i[1]]; b1 = t2[i[0]]; b2 = t2[i[1]] # значения индексов

    print(f"111  a1: {a1} || a2: {a2}")
    print(f"111  b1: {b1} || b2: {b2}")

    if yy == a1:
        if isinstance(b1, str) and isinstance(b2, str):
            return "-"
        if isinstance(b1, float) and isinstance(b2, str):
            return b1
        if isinstance(b1, str) and isinstance(b2, float):
            lineEditEnd.setStyleSheet("background-color: rgb(255, 170, 0);")
            return b2
    
    if (isinstance(b1, float) and isinstance(b2, str)):
        lineEditEnd.setStyleSheet("background-color: rgb(255, 170, 0);")
        try:
            b2 = float(b2)
        except:
            b2 = b1
    if (isinstance(b1, str) and isinstance(b2, float)):
        lineEditEnd.setStyleSheet("background-color: rgb(255, 170, 0);")
        try:
            b1 = float(b1)
        except:
            b1 = b2

    print(f"a1: {a1} || a2: {a2}")
    print(f"b1: {b1} || b2: {b2}")

    try:
        y = round(b2 + ((yy - a2) * (b1 - b2) / (a1 - a2)), 4)
        # y = round(b2 + ((yy - a2) * abs(b1 - b2) / abs(a1 - a2)), 4)
    except:
        y = "-"  
    return y

def GO(RowKey, columnKey, columnValue, YOOY, XOOX, lineEditEnd):
    
    lineEditEnd.setStyleSheet("background-color: rgb(220, 220, 220);")
    dct = {columnKey[i] : columnValue[i] for i in range(len(columnValue))}
    #===============================================================================
    '''Находим индексы колонок'''
    indexColumnKey = index_search(columnKey, XOOX)
    # print(f"indexColumnKey = {indexColumnKey}")
    a1 = columnKey[indexColumnKey[0]]
    a2 = columnKey[indexColumnKey[1]]

    # print(f"dct[a1] = {dct[a1]}")
    # print(f"dct[a2] = {dct[a2]}")

    try:
        #===============================================================================
        '''Находим промежуточные значение построчно'''
        tx = []
        tx.append(interpoi(RowKey, dct[a2], YOOY, lineEditEnd))
        tx.append(interpoi(RowKey, dct[a1], YOOY, lineEditEnd))
        #===============================================================================
        '''Находим вторую интерполяцию из найденных построчных промежутков в колонках'''
        res = interpoi([a2, a1], tx, XOOX, lineEditEnd) # результат интерполяции
        print(f"res = interpoi([a2={a2}, a1={a1}], tx={tx}, XOOX={XOOX})")
        res = round(res, 4)
        print(f"res | {YOOY} | {XOOX} |= {res}")
    except:
        res = "-"
    return str(res)
    #===============================================================================
if __name__ == "__main__":
    import os
    os.system('CLS') 
