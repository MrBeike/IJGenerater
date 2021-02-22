import hashlib
from datetime import datetime


def decimal(num: int, digit: int):
    formated = f'{num:.{digit}f}'
    return formated


def decimal0(num: int):
    return int(num)


def decimal2(num: int):
    return decimal(num, 2)


def decimal5(num: int):
    return decimal(num, 5)


def idMask(type: str, id: str) -> str:
    '''
    对用户证件信息进行脱敏处理。
    如果为身份证B01,则取前14位+32位MD5值，其他证件则只取MD5值。
    证件号空的话则返回空值。
    :param type:证件类型
    :param id:证件号
    :return:脱敏后的证件号
    '''
    id = id.replace(" ", "")
    content = id.upper()
    if id:
        md5 = hashlib.md5(content.encode('utf-8')).hexdigest()
        if type in ['B01', ]:
            # 或者按照类型dict决定截取数据长度,若后面改需求的话
            preValue = content[:14]
            idMasked = preValue + md5
        else:
            idMasked = md5
    else:
        idMasked = id
    return idMasked


def dateParser(date: str) -> str:
    '''
    日期格式化
    :param date:待处理的日期字符串
    :return: 处理后的日期字符串
    '''
    try:
        dateParsered = datetime.strftime(date, '%Y-%m-%d')
    except TypeError:
        dateParsered = date
    return dateParsered
