import pickle
import pandas as pd
import numpy as np
from parse import parse, compile
from .hooks import decimal0, decimal2, decimal5, idMask, dateParser


def hookParser(string):
    '''
    解析报表规范字符串表示，用于后续hook函数的编写
    '''
    fixed = ['I','F']
    patterns = ['C{n:d}','C..{n:d}','I..{n:d}','D{w:d}.{d:d}']
    if string in fixed:
        return {string:0}
    else:
        for pattern in patterns:
            regex = compile(pattern)
            result = regex.parse(string)
            if result != None:
                return result.named


def hookMaker(format):
    '''
    根据报表规范字符串解析结果，构建hook函数
    （目前只有整数、小数需要处理，其他属于合规性核验，暂时不管）
    '''
    keys = [key for key in format.keys()]
    key = keys[-1]
    if key == 'I':
        hook = 'decimal0'
    elif key == 'd':
        hook = f'decimal{format["d"]}'
    else:
        hook = 'False'
    return eval(hook)


def getReportName(filename):
    '''
    获取报表名称对应的字符串
    :param filename: str 报表名对应字符串关系表
    :return relationship:dict {报表中文名:报表字符串名}
    '''
    nameRelation = pd.read_excel(filename,header=0)
    name = nameRelation['报表名称'].to_list()
    string = nameRelation['表名对应字符串'].to_list()
    relationship = dict(zip(name,string))
    return relationship


def getReportRule(filename,relationship):
    '''
    根据报表规范文件解析出对应数据hook函数
    :param filename: str 报表规范文件表
    :parm relationship:dict {报表中文名:报表字符串名}
    :return 
    '''
    rules = {}
    all = pd.read_excel(filename,sheet_name=None)
    sheetNames = all.keys()
    for sheetName in sheetNames:
        stringName = relationship.get(sheetName)
        df = pd.read_excel(filename,sheet_name=sheetName)
        df.drop(df[np.isnan(df['序号'])].index, inplace=True)
        df['hook'] = df['长度'].apply(lambda x: hookMaker(hookParser(x)))
        df = df.drop(df[df.hook == False].index)
        index = df['序号'].apply(int).to_list()
        hook = df['hook'].to_list()
        rule = dict(zip(index,hook))
        rules[stringName] = rule
    return rules
    

def configWriter(obj, filename):
    fileHandler = open(filename, 'wb')
    pickle.dump(obj, fileHandler)
    fileHandler.close()
    return


def configReader(filename):
    fileHandler = open(filename, 'rb')
    rule = pickle.load(fileHandler)
    fileHandler.close()
    return rule


if __name__ == '__main__':
    relationship = getReportName('报表表名字符串对应关系表.xlsx')
    rules = getReportRule('报表规范.xls',relationship)
    configWriter(rules,'rule')