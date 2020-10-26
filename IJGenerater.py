from configparser import ConfigParser
from zipfile import ZipFile
import pandas as pd
import os, sys

class IJGenerater:
    def __init__(self,fileUrl):
        '''
        初始化变量
        :params fileUrl: Excel文件地址
        '''
        self.fileUrl = fileUrl
        # FIXME pyinstaller打包os模块提示木马(360报毒)
        filepath, filename_full = os.path.split(fileUrl)    
        filename, extension = os.path.splitext(filename_full)
        # 解析文件名获取相关信息
        self.creditCode = filename[0:18]
        self.date = filename[18:26]
        self.reportCode = filename[26:31]
        self.common_name = f"{self.creditCode}{self.date}{self.reportCode}"

    def appPath(self, relativepath):
        '''
        项目基础位置定位。(解决打包后找不到相对路径下的文件)
        '''
        if hasattr(sys, 'frozen'):
            basePath = os.path.dirname(sys.executable)
            # Handles PyInstaller
        else:
            basePath = os.path.dirname(__file__)
        print(os.path.join(basePath, relativepath))
        return os.path.join(basePath, relativepath)

    def configWriter(self):
        '''
        修改报表配置(Conifg.ini)
        '''
        writer = ConfigParser()
        # TODO        
        pass

    def configReader(self):
        '''
        读取报表配置(Conifg.ini)
        '''
        reader = ConfigParser()
        reader.read(self.appPath('resource//config.ini'),encoding='utf-8')
        self.keyword = reader['common']['keyword']
        section = reader[self.reportCode]
        self.dataProperty = section['dataProperty']
        self.currency = section['currency']
        self.unit = section['unit']
        self.flag = section['flag']
        self.dataType = section['dataType']

    def idxGenerater(self,path=''):
        '''
        根据报表信息组装I文件(idx后缀)
        '''
        # 组合I文件名称
        destFile = f'BI{self.common_name}.idx'
        content = f'{self.keyword}|{self.reportCode}|{self.dataProperty}|{self.currency}|{self.unit}|{self.flag}|{self.dataType}|{self.creditCode}'
        with open(os.path.join(path,destFile),'w',newline='',encoding='utf-8') as f:
            f.write(content)

    def Excel2Dat(self,path=''):
        '''
        将Excel文件转换成J文件(实质是csv文件,后缀使用dat)
        '''
        keyword = self.keyword
        # 组合J文件名称
        destFile = f"BJ{self.common_name}.dat"
        # 读取Excel文件内容并处理
        # TODO 是否根据reportCode来设置不同的converters(目前用处不大)
        df = pd.read_excel(self.fileUrl,header=1,sheet_name=0,skiprows=[0],converters={'本期情况':str})
        column_names = list(df)
        df.drop(columns=column_names[1],inplace=True)
        keyword_list = [keyword]* len(df)
        df.insert(0,column='keyword',value=keyword_list)
        content = df.to_csv(None,header=False,index=False,sep='|',encoding='utf-8',float_format='%.2f')
        # to_csv会自动多空一行，手动去除后两行写入文件
        with open(os.path.join(path,destFile),'w',newline='',encoding='utf-8') as f:
            f.write(content[:-2])    

    def zipFiles(self,path=''):
        '''
        将I文件和J文件打包压缩
        '''
        destFile = f'BI{self.common_name}.zip'
        idx_file = f'BI{self.common_name}.idx'
        dat_file = f'BJ{self.common_name}.dat'
        with ZipFile(os.path.join(path,destFile),'w') as f:
            f.write(os.path.join(path,idx_file))
            f.write(os.path.join(path,dat_file))

    def start(self,path=''):
        self.configReader()
        self.idxGenerater(path)
        self.Excel2Dat(path)
        self.zipFiles(path)


if __name__ == '__main__':
    title = '''
  __        ___  ________  _______   ________   _______   ________  ________  _________  _______   ________     
|\  \      |\  \|\   ____\|\  ___ \ |\   ___  \|\  ___ \ |\   __  \|\   __  \|\___   ___\\  ___ \ |\   __  \    
\ \  \     \ \  \ \  \___|\ \   __/|\ \  \\ \  \ \   __/|\ \  \|\  \ \  \|\  \|___ \  \_\ \   __/|\ \  \|\  \   
 \ \  \  __ \ \  \ \  \  __\ \  \_|/_\ \  \\ \  \ \  \_|/_\ \   _  _\ \   __  \   \ \  \ \ \  \_|/_\ \   _  _\  
  \ \  \|\  \\_\  \ \  \|\  \ \  \_|\ \ \  \\ \  \ \  \_|\ \ \  \\  \\ \  \ \  \   \ \  \ \ \  \_|\ \ \  \\  \| 
   \ \__\ \________\ \_______\ \_______\ \__\\ \__\ \_______\ \__\\ _\\ \__\ \__\   \ \__\ \ \_______\ \__\\ _\ 
    \|__|\|________|\|_______|\|_______|\|__| \|__|\|_______|\|__|\|__|\|__|\|__|    \|__|  \|_______|\|__|\|__|                                                                                                        
'''
    while True:
        print(title)
        fileUrl = input('请输入文件路径(支持拖入文件哦)：')
        keyword = 'I00001'
        g = IJGenerater(fileUrl,keyword)
        g.start()
        print('文件成功生成,请在程序所在目录查找')