import os
import zipfile

# def workDirClean():
#     fileList = os.listdir(workDir)
#     for eachfile in fileList:
#         try:
#             suff = eachfile.split('.')[1]
#             if suff in ['dat', 'log']:
#                 os.remove(eachfile)
#         except IndexError:
#             pass


# def getfileNames():
#     '''
#     获取工作文件夹下所有的xlsx格式文件

#     '''
#     fileList = os.listdir(workDir)
#     excelFiles = []
#     for eachfile in fileList:
#         try:
#             suff = eachfile.split('.')[1]
#             if suff == 'xlsx':
#                 excelFiles.append(eachfile)
#         except IndexError:
#             pass
#     return excelFiles

def zipFile(filename, path=''):
    zipFilename = f'{os.path.join(path, filename)}.zip'
    zipFile = zipfile.ZipFile(zipFilename, 'w', zipfile.ZIP_DEFLATED)
    f_txt = filename + '.dat'
    f_log = filename + '.log'
    try:
        zipFile.write(os.path.join(path, f_txt), arcname=f_txt)
        zipFile.write(os.path.join(path, f_log), arcname=f_log)
        zipFile.close()
        print(f'{filename}报表压缩包搞定啦！')
    except:
        print(f'{filename}报表dat文件或log文件丢失，请尝试重新运行本程序')
