import os
import pandas as pd
from .hooksConfig import configReader
from .hooks import decimal0, decimal2, decimal5, idMask, dateParser


def datWriter(filename, reportConfig, path=''):
    df = pd.read_excel(filename, header=0, sheet_name=0)
    columnNames = list(df)
    for key, value in reportConfig.items():
        columnName = columnNames[key-1]
        # FIXME idMask函数补丁 如何区分各类证件？
        # BUG 证件类型和证件号不一定是前后关系？
        if value.__name__ == 'idMask':
            assistColumnName = columnNames[key-2]
            assistDF = df[assistColumnName]
            dataDF = df[columnName]
            idRule = zip(assistDF,dataDF)
            idMasked = [value(x,y) for x,y in idRule]
            df[columnName] = idMasked
        else:
            df[columnName] = df[columnName].map(lambda x: value(x))
    content = df.to_csv(None, header=False, index=False,
                        sep='|', encoding='utf-8')
    # to_csv会自动多空一行，手动去除后两行写入文件
    datFilename = os.path.join(path, filename.replace('xlsx', 'dat'))
    # 清理已存在的同名dat文件，保证创建时间准确性
    existsFlag = os.path.exists(datFilename)
    if existsFlag:
        os.remove(datFilename)
    with open(datFilename, 'w', newline='', encoding='utf-8') as f:
        f.write(content[:-2])


if __name__ == '__main__':
    rules = configReader('rule')
    rule = rules['CLGRDK']
    filename = '91341700573031656T_CLGRDK_20201130.xlsx'
    datWriter(filename,rule)
