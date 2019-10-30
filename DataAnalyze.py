import sys
import os
import csv
from PyQt5.QtWidgets import (QFileDialog, QMainWindow, QApplication, QMessageBox, QSpinBox, QGridLayout,QSizePolicy)
from PyQt5 import QtGui

from Ui_DataAnalyze import Ui_DataAnalyze #从自动生成的界面文件导入基础界面
from MyFigure import PlotCanvas #从图表文件中导入图表类
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

class MyWindow(QMainWindow, Ui_DataAnalyze, QFileDialog):
    
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setupUi(self)
        self.ui_init()
        self.SetConnect()
        self.show()

    def ui_init(self):
        self.lineEdit_StartTime.setText("7")
        self.lineEdit_EndTime.setText("18")
        self.lineEdit_CanID.setText("14019C94")
        self.progressBar.setValue(0)
        self.plot = PlotCanvas(self, width=5, height=4)
        self.verticalLayout.addWidget(self.plot)
        self.mpl_ntb = NavigationToolbar(self.plot, self)
        self.verticalLayout.addWidget(self.mpl_ntb)

    def SetConnect(self):    
        self.DirButton.clicked.connect(self.OpenDirPath)
        self.pushButton_Process.clicked.connect(self.DataAnalyzeClick)

    def OpenDirPath(self):
        srcDirPath = QFileDialog.getExistingDirectory(self, "选择数据文件夹","/")
        self.lineEdit_FileDir.setText(srcDirPath)

    def DataAnalyzeClick(self):
        self.content=[[],[],[]]
        total_number = 0
        h_start = int(self.lineEdit_StartTime.text())
        h_end = int(self.lineEdit_EndTime.text())
        can_id = self.lineEdit_CanID.text()
        for h in range(h_start, h_end):
            for m in range(0, 60):      #分钟
                file_path = self.lineEdit_FileDir.text()+'\\%.2d_%.2d.csv'%(h,m)
                if os.path.exists(file_path):
                    total_number += 1

        print("total_number = %s"%(total_number))
        self.progressBar.setRange(0, (total_number-5)*600) #1个发送文件600个 14019C94 匹配

        for h in range(h_start, h_end):             #时间区间 左闭右开
            for m in range(0, 60):                  #分钟
                file_path = self.lineEdit_FileDir.text()+'\\%.2d_%.2d.csv'%(h,m)    #获取文件路径
                if os.path.exists(file_path):       #检查文件是否存在，若存在则打开读取其中的数据
                    file_open = open(file_path,'r')
                    csv_file=csv.reader(file_open)
                    for line in csv_file:
                        data = {}
                        for line in csv_file:
                            if line[3] == '1401949C':
                                # print(line[1])
                                A_2 = '%.2x%.2x'%(int(line[7], 16),int(line[8],16))
                                A_2 = int(A_2,16) - 1000
                                data['A_2'] =  A_2
                                V_2 = '%.2x%.2x'%(int(line[5], 16),int(line[6],16))
                                V_2 = int(V_2,16)
                                data['V_2'] =  V_2
                            if line[3] == '1802E0E1':  #800V1
                                A_1 = '%.2x%.2x'%(int(line[5], 16),int(line[6],16))
                                A_1 = int(A_1,16) - 32000#800V1
                                data['A_1'] =  A_1
                                V_1 = '%.2x%.2x'%(int(line[7], 16),int(line[8],16))
                                V_1 = int(V_1,16)
                                data['V_1'] =  V_1
                                W = ((data['V_1']  +  data['V_2']) /2) * (data['A_1']  - data['A_2']  ) /1000
                                self.content[0].append(W)
                                self.progressBar.setValue(len(self.content[0]))
                                self.textEdit.insertPlainText(line[1] + ',%.03f'%W +'\r\n')
                        # if line[3] == can_id:  #动力单元功率
                        #     number = '%.2x%.2x'%(int(line[5], 16),int(line[6],16))
                        #     no = int(number, 16)-500 #动力单元功率
                        #     if no >= 0:
                        #         self.textEdit.insertPlainText(line[1]+'\r\n')
                        #         # print(line[1])
                        #     self.content[0].append(no)
                        #     self.progressBar.setValue(len(self.content[0]))
        self.plot.plot(data = self.content[0])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myshow = MyWindow()
    sys.exit(app.exec_())