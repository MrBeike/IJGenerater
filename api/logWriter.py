import os
import time
import hashlib


def getFileMD5(filename: str) -> str:
    """
    计算文件的md5
    :param file_name:文件名
    :return:md5值
    """
    count = 0
    m = hashlib.md5()  # 创建md5对象
    with open(filename, 'rb') as f:
        while True:
            data = f.read(4096)
            if not data:
                break
            m.update(data)  # 更新md5对象
            # count += data.count(b'\n')
    return m.hexdigest()  # 返回md5对象


def logWriter(filename: str, path: str = ''):
    '''
    生成待转换报表的log文件
    :param filename:文件名
    :param path: 路径(Console默认根目录,Gui可配置)
    :return:
    '''
    fileName = filename
    fileMD5, _ = getFileMD5(fileName)
    fileSize = os.path.getsize(filename)
    fileCtime = time.strftime(
        '%Y-%m-%d %H:%M:%S', time.localtime(os.path.getctime(filename)))
    # 大文件存在性能问题
    fileEntry = len(open(filename, 'r', encoding='utf-8').readlines())
    logInfo = [fileName, fileMD5, fileSize, fileCtime, fileEntry]
    content = '\n'.join(str(x) for x in logInfo)
    logFilename = os.path.join(path, filename.replace('dat', 'log'))
    with open(logFilename, 'w', encoding='utf-8') as f:
        f.write(content)
    return


if __name__ == '__main__':
    logWriter('personal.dat')
