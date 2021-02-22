from api.zipFile import zipFile
from api.logWriter import logWriter
from api.hooksConfig import configReader, configWriter
from api.datWriter import datWriter
import os


class FUDT:
    def __init__(self):
        self.configFilename = 'resource\\rule'

    def getFileInfo(self):
        fileUrl = input('请输入EXCEl文件完整路径(支持拖拽文件哦)：')
        if fileUrl:
            filePath, filename = os.path.split(fileUrl)
            pureFilename, extension = os.path.splitext(filename)
            orgCode, reportCode, date = filename.split('_')
            self.filePath = filePath
            self.filename = filename
            self.pureFilename = pureFilename
            self.reportCode = reportCode
            self.date = date
        else:
            print('文件路径错误或不支持。')
        return

    def configHandler(self):
        # TODO 提供更新规则选择入口
        # configWriter(rules,self.configFilename)
        config = configReader(self.configFilename)
        self.reportConfig = config[self.reportCode]
        return

    def datFileGenerater(self):
        datWriter(self.filename, self.reportConfig, path=self.filePath)

    def logFileGenerater(self):
        datFilename = f'{self.pureFilename}.dat'
        logWriter(datFilename, path=self.filePath)

    def zipFileGenerater(self):
        zipFile(self.pureFilename, path=self.filePath)

    # TODO 新建工作子目录 Or 当前目录处理并清理
    def workDirClean(self):
        pass


if __name__ == '__main__':
    fudt = FUDT()
    fudt.getFileInfo()
    fudt.configHandler()
    fudt.datFileGenerater()
    fudt.logFileGenerater()
    fudt.zipFileGenerater()
    fudt.workDirClean()