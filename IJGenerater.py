from configparser import ConfigParser
from zipfile import ZipFile
import pandas as pd

class IJGenerater:
    def __init__(self,fileUrl,keyword):
        '''
        初始化变量
        :params fileUrl: Excel文件地址
        :params keyword: 表单关键词代码
        '''
        self.fileUrl = fileUrl
        self.keyword = keyword
        # FIXME pyinstaller打包os模块提示木马(360报毒)
        # path, filename = os.path.split(fileUrl)
        filename = fileUrl.split('\\')[-1]
        filename_name = filename.split('.')[0]
        # filename_part = filename_name.split('#')
        # self.creditCode, self.date, _, self.reportCode = filename_part
        # self.common_name = f"{self.creditCode}{self.date.replace('-','')}{self.reportCode}"
        # 解析文件名获取相关信息
        self.creditCode = filename_name[0:18]
        self.date = filename_name[18:26]
        self.reportCode = filename_name[26:31]
        self.common_name = f"{self.creditCode}{self.date}{self.reportCode}"

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
        reader.read('config.ini',encoding='utf-8')
        section = reader[self.reportCode]
        self.dataProperty = section['dataProperty']
        self.currency = section['currency']
        self.unit = section['unit']
        self.flag = section['flag']
        self.dataType = section['dataType']

    def idxGenerater(self):
        '''
        根据报表信息组装I文件(idx后缀)
        '''
        # 组合I文件名称
        destFile = f'BI{self.common_name}.idx'
        content = f'{self.keyword}|{self.reportCode}|{self.dataProperty}|{self.currency}|{self.unit}|{self.flag}|{self.dataType}|{self.creditCode}'
        with open(destFile,'w',newline='',encoding='utf-8') as f:
            f.write(content)

    def Excel2Dat(self):
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
        with open(destFile,'w',newline='',encoding='utf-8') as f:
            f.write(content[:-2])    

    def zipFiles(self):
        '''
        将I文件和J文件打包压缩
        '''
        with ZipFile(f'BI{self.common_name}.zip','w') as f:
            f.write(f'BI{self.common_name}.idx')
            f.write(f'BJ{self.common_name}.dat')

    def start(self):
        self.configReader()
        self.idxGenerater()
        self.Excel2Dat()
        self.zipFiles()


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