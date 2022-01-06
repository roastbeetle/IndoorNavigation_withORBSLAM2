#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from PyQt4.QtGui import *
from PyQt4 import QtGui, QtCore
import subprocess
import rospy
from std_msgs.msg import Int32MultiArray as intarr
#from dest_list_ui import Ui_Form

#import navigator_ui
#import dest_list_ui
import dest_list_ui2

class dest_list_dialog(QWidget, dest_list_ui2.Ui_Form):
    def __init__(self,dest_list):
        super(dest_list_dialog, self).__init__()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.lay = QtGui.QHBoxLayout()
        self.sA = QtGui.QScrollArea()
        self.status = 0
        self.dests = dest_list
        self.cur = [0,0,0,0,0]
        self.arr_cnt = 0
        #self.thread = QtCore.QThread()
        self.mysig = QtCore.SIGNAL("do_Update")
        self.pushButtonx = QtGui.QPushButton(self)
        QtCore.QObject.connect(self.pushButtonx, self.mysig, self.update)
        rospy.Subscriber('instruct',intarr,self.int_callback,queue_size =1)

        #self.sA_Lay = QtGui.QVBoxLayout()
       # self.sA.setLayout(self.sA_Lay)D
       # self.lay.addWidget(self.sA)
        #self.setLayout(self.lay)
        #QWidget.__init__(self)
        # setupUi() 메서드는 화면에 다이얼로그 보여줌
        self.setupUi(self, dest_list)  

    def int_callback(self,data): # [seq, back, cur_dis, left_right]
        if self.cur != data.data:
            self.pushButtonx.emit(self.mysig)
        self.cur = [data.data[0],data.data[1],data.data[2],data.data[3],data.data[4]]

    def update(self): 
        self.hide_arrow()
        self.hide_text()  
        if self.cur[0] == 1000:
            self.print_arrived()
        elif self.cur[0] == 0:
            self.print_straight_arrow()
        else:
            if self.cur[3] == 1:
                self.print_right_arrow()
                self.print_meter_text(self.cur[2])
            elif self.cur[3] == 0:
                self.print_left_arrow()
                self.print_meter_text(self.cur[2])
            else :
                self.print_straight_arrow()
                self.print_meter_text(self.cur[2])

    def add_list_item(self,button_name):
        
        button = QtGui.QPushButton(button_name)
        self.sA_Lay.addWidget(button)
        return

    def hide_arrow(self):
        #화살표를 숨기는 메소드. 다른 화살표를 띄우기 전에 실행

        try:
            self.lbl.hide()

        except:
            pass
    def hide_text(self):
        #텍스트를 숨기는 메소드. 남은 거리를 바꾸기 전에 실행
        try:
            self.lbl_text.hide()

        except:
            pass

    def print_arrived(self):
        #"도착" 글씨를 띄우는 메소드
        self.lbl = QLabel(self)
        self.lbl.resize(600,800)  
        if self.cur[4]%3 == 0:
            pixmap = QPixmap("11.png")
        elif self.cur[4]%3 == 1:
            pixmap = QPixmap("12.png")
        else :
            pixmap = QPixmap("13.png")
        self.lbl.setPixmap(pixmap)
        
        #self.lbl.resize(400,300)
        self.lbl.show()          

    def print_right_arrow(self):
        #오른쪽 화살표 띄우는 메소드
        self.lbl = QLabel(self)
        self.lbl.resize(600,800)  
        pixmap = QPixmap("4.png")
        self.lbl.setPixmap(pixmap)
        
        #self.lbl.resize(600,1024)  
        self.lbl.show()       


    def print_left_arrow(self):
        #왼쪽 화살표 띄우는 메소드
        #print('left')
        self.lbl = QLabel(self)
        self.lbl.resize(600,800)  
        pixmap = QPixmap("3.png")
        self.lbl.setPixmap(pixmap)
        #self.lbl.setGeometry()
        #self.lbl.resize(600,1024)  
        self.lbl.show() 

    def print_straight_arrow(self):
        #직진 화살표 띄우는 메소드
        self.lbl = QLabel(self)
        self.lbl.resize(600,800)   # 이미지를 보여주기 위해 출력될 label의 크기를 400×400으로 설정
        #self.lbl.setGeometry(200,200,600,600)
        pixmap = QPixmap("5.png")
        self.lbl.setPixmap(pixmap)
        
        #self.lbl.resize(600,1024)   # 이미지를 보여주기 위해 출력될 창의 크기를 400×400으로 설정
        self.lbl.show() 

    def print_meter_text(self,meter):
        txs = 0
        if meter > 9:
            txs = 180
        else:
            txs = 220
        self.lbl_text = QLabel(self)
        self.lbl_text.resize(100,100)
        text_to_print = str(meter) +"m"
        text_to_print = text_to_print.decode('utf-8')
        self.lbl_text.setText(text_to_print)
        self.lbl_text.setFont(QtGui.QFont("맑은고딕",80))
        self.lbl_text.setGeometry(txs,750,300,100)
        self.lbl_text.show()

    def home(self):
        #홈버튼이 눌렸을 때 할 행동
        self.status = 0
        self.hide_arrow()
        self.hide_text()
        self.publish_dest(1000)
        pass
    
    def publish_dest(self,idx):
        global dest_pub
        global app
        destination = intarr()
        destination.data = [0,0,0] 
        if idx == 1000:
            dest_pub.publish(destination)
        else:  
            destination.data[0]=int(self.dests[idx][1])
            destination.data[1]=int(self.dests[idx][2])
            print(destination)
            dest_pub.publish(destination)

    def btn1(self):
        self.publish_dest(0)
    def btn2(self):
        self.publish_dest(1)
    def btn3(self):
        self.publish_dest(2)
    def btn4(self):
        self.publish_dest(3)

class CustomWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(CustomWidget, self).__init__(parent)
        self.button = QtGui.QPushButton("buttaon")
        lay = QtGui.QHBoxLayout(self)
        lay.addWidget(self.button, alignment=QtCore.Qt.AlignRight)
        lay.setContentsMargins(0, 0, 0, 0)

class Dialog_list(QtGui.QDialog):
    def __init__(self, parent=None):
        super(Dialog_list, self).__init__(parent=parent)
        vLayout = QtGui.QVBoxLayout(self)
        hLayout = QtGui.QHBoxLayout()
        self.lineEdit = QtGui.QLineEdit()
        hLayout.addWidget(self.lineEdit)
        self.filter = QtGui.QPushButton("filter", self)
        hLayout.addWidget(self.filter)
        self.list = QtGui.QListView(self)
        vLayout.addLayout(hLayout)
        vLayout.addWidget(self.list)
        self.model = QtGui.QStandardItemModel(self.list)
        codes = [
            'windows',
            'windows xp',
            'windows7',
            'hai',
            'habit',
            'hack',
            'good'
        ]
        self.list.setModel(self.model)
        for code in codes:
            item = QtGui.QStandardItem(code)
            self.model.appendRow(item)
            self.list.setIndexWidget(item.index(), CustomWidget())

class Window(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.list = QtGui.QListWidget(self)
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.list)

    def addListItem(self, text):
        item = QtGui.QListWidgetItem(text)
        self.list.addItem(item)
        widget = QtGui.QWidget(self.list)
        button = QtGui.QToolButton(widget)
        layout = QtGui.QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addStretch()
        layout.addWidget(button)
        self.list.setItemWidget(item, widget)
        button.clicked[()].connect(
            lambda: self.handleButtonClicked(item))

    def handleButtonClicked(self, item):
        print(item.text())

class TestGui(QtGui.QWidget):
    """ A Fast test gui show how to create buttons in a ScrollArea"""
    def __init__(self):
        super(TestGui, self).__init__()
        self.lay = QtGui.QHBoxLayout()
        self.sA = QtGui.QScrollArea()
        self.sA.widgetResizable = False
        self.sA_lay = QtGui.QHBoxLayout()
        self.sA.setLayout(self.sA_lay)
        self.sA.setGeometry(QtCore.QRect(220,40,641,471))
        self.sA.setWidgetResizable(True)
        self.closeGui = QtGui.QPushButton("Close")
        self.add_file_button = QtGui.QPushButton("Add File")
        self.lay.addWidget(self.closeGui)
        self.lay.addWidget(self.add_file_button)
        self.lay.addWidget(self.sA)
        self.setLayout(self.lay)
        self.connect_()

    def connect_(self):
        self.add_file_button.clicked.connect(self.__add_file_to_list)
        self.closeGui.clicked.connect(self.close)
        return

    def __add_file_to_list(self,button_name):
        fname = QtGui.QFileDialog.getOpenFileName()
        global filenames
        filenames.append(fname)
        button = QtGui.QPushButton(fname)
        button.setMinimumSize(QtCore.QSize(0,450))
        
        self.sA_lay.addWidget(button)
        return

class Map_edit_gui(QtGui.QWidget):

    def __init__(self):
        super(Map_edit_gui, self).__init__()
        self.lay = QtGui.QHBoxLayout()
        self.sA = QtGui.QScrollArea()
        self.sA_lay = QtGui.QVBoxLayout()
        self.sA.setLayout(self.sA_lay)
        self.closeGui = QtGui.QPushButton("Close")
        self.add_file_button = QtGui.QPushButton("Add File")
        self.lay.addWidget(self.closeGui)
        self.lay.addWidget(self.add_file_button)
        self.lay.addWidget(self.sA)
        self.setLayout(self.lay)
       # self.connect_()

    #def connect_(self):
     #   self.add_file_button.clicked.connect(self.__add_file_to_list)
      #  self.closeGui.clicked.connect(self.close)
       # return

    def __add_file_to_list(self,button_name):
        fname = QtGui.QFileDialog.getOpenFileName()
        #global filenames
        #filenames.append(fname)
        button = QtGui.QPushButton(button_name)
        self.sA_lay.addWidget(button)
        return

class img_lay(QMainWindow):
    def __init__(self):
        super(img_lay,self).__init__()
        self.initUI()

    def initUI(self):
        self.lbl = QLabel(self)
        self.lbl.resize(400,400)   # 이미지를 보여주기 위해 출력될 label의 크기를 400×400으로 설정
        pixmap = QPixmap("aa.png")
        self.lbl.setPixmap(pixmap)

        self.resize(400,400)   # 이미지를 보여주기 위해 출력될 창의 크기를 400×400으로 설정
        #self.show()

class dest_arrow_lay(QMainWindow):
    def __init__(self):
        super(dest_arrow_lay,self).__init__()
        self.initUI()

    def initUI(self):
        self.lbl = QLabel(self)
        self.lbl.resize(211,464)   # 이미지를 보여주기 위해 출력될 label의 크기를 400×400으로 설정
        pixmap = QPixmap("arrow.png")
        self.lbl.setPixmap(pixmap)

        self.resize(600,1024)   # 이미지를 보여주기 위해 출력될 창의 크기를 400×400으로 설정
        #self.show()        

class navigation_arrow(QtGui.QWidget):
    def __init__(self):
        super(navigation_arrow, self).__init__()
        img_widget = QWidget()
        img_widget.setWindowTitle("Navigating Mode")
        label = QLabel(img_widget)
        pixmap = QPixmap('./gui/grid_map.jpg')
        label.setPixmap(pixmap)
        img_widget.resize(pixmap.width(),pixmap.height()) 
        img_widget.show()       

rospy.init_node('navigation_gui')
dest_pub = rospy.Publisher("/target_point",intarr,queue_size =1)
app = QApplication(sys.argv)
if __name__ == "__main__":
    #initialize
    f = open('/home/lb/.ros/dest_list.txt','r')
    dest_list = []
    dests = f.readlines()
    for dest in dests:
        dest_list.append(dest.strip().split(','))
    print(dest_list)
    #dlg = XDialog()
    meg = Map_edit_gui()
    img_layout = img_lay()
    arrow_dialog = dest_arrow_lay()
    dest_dialog = dest_list_dialog(dest_list)
    
    dest_dialog.show()
    #dest_dialog.showMaximized()
    # 전체화면으로 실행 

    list_appendable = TestGui()
    #list_appendable.show()
    arr = navigation_arrow()
    #arr.show()
    #ad = listDialog()
    #for i in range(1,2):
    #    ad.add_list_item("asd")
   # ad.show()

    

    #dest_list_dialog.add_file_to_list("dest1")
    #dest_list_dialog.add_file_to_list("dest2")
    ##dest_list_dialog.add_file_to_list("dest3")
    #dest_list_dialog.add_file_to_list("dest4")
    #dlg.show()
    app.exec_()

    #sys.exit(app.exec_())

#
#길안내 화면
#목적지 선택

#목적지 입력k


#할일
#목적지 불러와서 버튼 만들고 스크롤
#점찍기
#우분투에 파이큐티 설치


#코너에서 좌회전 -> n미터 앞에서 
#인터넷 연결없을떄 돌아가게
#우분투 시작프로그램
#우분투 자동잠금
