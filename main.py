from PyQt5.QtWidgets import QApplication, QWidget,QMessageBox,QFileDialog
from PyQt5.QtCore import QTime
from Frame import Ui_Form
import os
import sys

# pyuic5 -x ui.ui -o Frame.py
# Pyinstaller -F -i logo.ico  main.py -p Frame.py

class MyMainForm(QWidget, Ui_Form):
    def __init__(self):
        super(MyMainForm, self).__init__()
        self.setupUi(self)
        #self.resize(600,800)
        self.setFixedSize(360,220)   # 固定大小
        self.slot_init()             # 初始化槽函数

        self.selectFileName=''

       
    
    '''初始化所有槽函数'''
    def slot_init(self):
        self.upload.clicked.connect(self.UP)
        self.ok.clicked.connect(self.OK)
     
    # 导入文件
    def UP(self):
        self.selectFileName,_ = QFileDialog.getOpenFileName(self,'选择文件','./')
        if self.selectFileName == '':
                QMessageBox.information(self,"提示","请选择文件",QMessageBox.Yes)
        elif(self.selectFileName.lower().endswith(('.mp4', '.avi','flv'))==False):
                QMessageBox.warning(self,'警告','请输入正确的视频格式',QMessageBox.Yes)
        else:
            # 清空界面
            self.i_name.setText('')
            self.o_name.setText('')
            self.result.setText('')
            self.s_time.setTime(QTime(0, 0, 0))
            self.e_time.setTime(QTime(0, 0, 0))
      
   
            # 展示导入的文件名
            # self.dir = selectFileName.rsplit('/',1)[0]  # 从后往前分割，且只分割一次，得到文件的路径信息。
            imputFileName = self.selectFileName.split('/')[-1]
            self.i_name.setText(imputFileName)
            self.o_name.setText(imputFileName.split('.')[0]+'(剪辑)'+'.'+imputFileName.split('.')[-1])


           

   # 函数示例
    def OK(self):

    
        if(self.i_name.text()==''):
            QMessageBox.information(self,"提示","请选择文件",QMessageBox.Yes)
            return

        # 保证结束时间大于开始时间
        s_time = self.s_time.time()
        e_time = self.e_time.time()
        if(s_time.secsTo(e_time)<=0):
            QMessageBox.warning(self,'警告','请保证结束时间大于开始时间',QMessageBox.Yes)
            return

  
        
        #执行剪辑
        path = self.selectFileName.rsplit('/',1)[0]  # 从后往前分割，且只分割一次，得到文件的路径信息。
        cmd = 'ffmpeg -i '+ self.selectFileName +' -ss '+ s_time.toString('hh:mm:ss') +' -to '+ e_time.toString('hh:mm:ss') +' -codec copy '+path+'/'+self.o_name.text()
        print(cmd)
        os.system(cmd)


        
  
        # 展示剪辑的结果
        self.result.setText("<font color=%s>%s</font>" %('#20B2AA', '剪辑完成！文件夹已打开'))

        # 通过cmd命令自动打开目标文件所在的文件夹
        os.system('start explorer '+path.replace('/','\\'))   # 小细节：在win中路径中需要用D:\test，不能用D:/test，否则这个cmd命令无效
        

    
if __name__=='__main__':
    app=QApplication(sys.argv)
    w=MyMainForm()
    w.show()
    sys.exit(app.exec_())