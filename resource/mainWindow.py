import sys
import resource.resource_rc 
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication,QMessageBox,QFileDialog
from PySide2.QtCore import Slot
from IJGenerater import IJGenerater

class IJwindow:
    def __init__(self):
        self.ui = QUiLoader().load('resource//main.ui')
        self.donate_ui = QUiLoader().load('resource//donate.ui')
        self.about_ui = QUiLoader().load('resource//about.ui')
        # self.ui.config_action.triggered.connect()
        self.ui.donate_action.triggered.connect(self.donate_ui.show)
        self.ui.about_action.triggered.connect(self.about_ui.show)
        self.ui.open_button.clicked.connect(self.open_file)
        self.ui.generater_button.clicked.connect(self.generate_file)
        self.ui.generater_button.setDisabled(True)

    @Slot()
    # 定义浏览文件对话框
    def open_file(self):
        # 打开文件
        fileUrl, selectedFilter = QFileDialog.getOpenFileName(self.ui, "打开EXCEL报表", "", "EXCEL文件(*.xls *.xlsx)")
        if fileUrl:
            self.generater = IJGenerater(fileUrl)
            self.ui.creditCode_line.setText(self.generater.creditCode)
            self.ui.reportCode_line.setText(self.generater.reportCode)
            self.ui.date_line.setText(self.generater.date)
            self.ui.generater_button.setDisabled(False)
    
    @Slot()
    def generate_file(self):
        path = QFileDialog.getExistingDirectory(self.ui, "IJ文件保存","", options=QFileDialog.ShowDirsOnly)
        self.generater.start(path)
        self.ui.generater_button.setDisabled(True)
        QMessageBox.information(self.ui,'提示', '完工啦！')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    IJwindow = IJwindow()
    IJwindow.ui.show()
    sys.exit(app.exec_())