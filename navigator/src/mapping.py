#!/usr/bin/env python
#-*- coding:utf-8 -*-
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')
#유니코드 에러 시 사용하는 코드
from PyQt4.QtGui import *
from PyQt4 import QtGui, QtCore

import mapping_ui

filenames = []

class mapping_ui(QWidget, mapping_ui.Ui_Dialog):
    

    def __init__(self):
        super(mapping_ui, self).__init__()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setupUi(self)
        self.painter = PaintTable(self)
        self.painter.setGeometry(50,200,500,500)
        self.painter.hide()


    def open_image_btn(self):
        print("open image btn pressed")
        #address = self.get_map_addr()
        address = self.painter.get_map_addr()
        #self.open_image(address)
        #self.painter.open_image(address)

        self.painter.show()
    
    def close_btn(self):
        if self.painter.pos != []:
            alert_warning = '저장 경고'.decode('utf-8')
            alert_content = '저장하지 않은 내용이 있습니다.\n저장하시겠습니까?'.decode('utf-8')
            buttonReply = QMessageBox.information(self, alert_warning, alert_content,   QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)

            if buttonReply == QMessageBox.Yes:
                print('Yes clicked.')
                self.painter.save_pos_addr(self.painter.pos_name , self.painter.pos)
            elif buttonReply == QMessageBox.No:
                print('No clicked.')
                sys.exit()
            elif buttonReply == QMessageBox.Cancel:
                print('Cancel clicked.')
        else:
            sys.exit()


    def save_btn(self):
        print("save button pressed")
        self.painter.save_pos_addr(self.painter.pos_name , self.painter.pos)
    
    def get_map_addr(self):
        addr = QtGui.QFileDialog.getOpenFileName()
        return addr

    def open_image(self,file_addr):
        try: #이미 open된 이미지를 닫음
            self.lbl.hide()
        except:
            pass

        

        self.lbl = QLabel(self)
        self.lbl.resize(500,500)
        #맵 이미지가 500x500이라고 가정
        pixmap = QPixmap(file_addr)
        self.lbl.setPixmap(pixmap)
        self.lbl.resize(500,500)
        self.lbl.setGeometry(50,200,500,500)
        self.lbl.show()


    


class PaintTable(QtGui.QTableWidget):
    #pixmap = QPixmap("aa.png")

    def __init__(self, parent):
        QtGui.QTableWidget.__init__(self, parent)
        self.center = QtCore.QPoint(-10,-10)
        self.addr = ""
        self.pos_name = []
        self.pos = []

    def open_image(self,file_addr):
        try: #이미 open된 이미지를 닫음
            self.lbl.hide()
        except:
            pass


        self.lbl = QLabel(self)
        self.lbl.resize(500,500)
        #맵 이미지가 500x500이라고 가정
        pixmap = QPixmap(file_addr)
        self.lbl.setPixmap(pixmap)
        self.lbl.resize(500,500)
        self.lbl.setGeometry(0,0,500,500)
        self.lbl.show()
         

    def paintEvent(self, event):
        painter = QtGui.QPainter(self.viewport()) #See: http://stackoverflow.com/questions/12226930/overriding-qpaintevents-in-pyqt
        pixmap = QPixmap(self.addr)
        painter.drawPixmap(self.rect(),pixmap)
        painter.drawEllipse(self.center,5,5)
        QtGui.QTableWidget.paintEvent(self,event)
        #pen = Qpen(Qt.red, 3)
        #painter.setPen(pen)
        #painter.drawEllipse(self.center,10,10)




    def mousePressEvent(self, event):
        if event.buttons() == QtCore.Qt.RightButton:
            self.center = QtCore.QPoint(event.pos().x(),  event.pos().y())
            print self.center
            self.viewport().repaint()
            pos_name = str(self.show_input_dialog()) 
            if pos_name != '':

                self.pos_name.append(pos_name)
                self.pos.append(str(self.center)[19:])


        elif event.buttons() == QtCore.Qt.LeftButton:
            QtGui.QTableWidget.mousePressEvent(self,event)


    def get_map_addr(self):
        addr = QtGui.QFileDialog.getOpenFileName()
        self.addr = addr
        return addr

    def show_input_dialog(self):
        dialog_name = "장소 저장".decode('utf-8')
        dialog_content = "저장할 위치의 이름을 입력해주세요".decode('utf-8')
        get_text_dialog = QInputDialog.getText(self, dialog_name, dialog_content)
        print(get_text_dialog)
        name_position, ok = str(get_text_dialog[0]) , get_text_dialog[1] 
        if ok:
            #print(name_position)
            return name_position
        else:
            return ''

    def save_pos_addr(self,pos_name,pos):
        f = open("dests.txt", 'a')
        for i in range(0,len(pos_name)):
            f.write(pos_name[i]+', '+pos[i][1:-1]+', 0\n')
        f.close()
        self.pos = []
        self.pos_name = []




class TestGui(QtGui.QWidget):
    """ A Fast test gui show how to create buttons in a ScrollArea"""
    def __init__(self):
        super(TestGui, self).__init__()
        self.setGeometry(300,300,600,1024)
        self.lay = QtGui.QHBoxLayout()
        self.sA = QtGui.QScrollArea()
        self.sA.widgetResizable = False
        self.sA_lay = QtGui.QHBoxLayout()
        self.sA.setLayout(self.sA_lay)
        self.sA.setGeometry(QtCore.QRect(220,40,841,971))
        self.sA.setWidgetResizable(True)
        self.closeGui = QtGui.QPushButton("Close")
        self.add_file_button = QtGui.QPushButton("Open File")
        self.lay.addWidget(self.closeGui)
        self.lay.addWidget(self.add_file_button)
        self.lay.addWidget(self.sA)
        self.setLayout(self.lay)
        self.connect_()

    def connect_(self):
        self.add_file_button.clicked.connect(self.get_map_addr())
        self.closeGui.clicked.connect(self.close)
        return

    def __add_file_to_list(self,button_name):
        fname = QtGui.QFileDialog.getOpenFileName()
    
        print(fname)
        global filenames
        filenames.append(fname)
        button = QtGui.QPushButton(fname)
        button.setMinimumSize(QtCore.QSize(0,0))
        
        self.sA_lay.addWidget(button)
        return

    def get_map_addr(self):
        addr = QtGui.QFileDialog.getOpenFileName()
        return addr

    def open_image(self,file_addr):
        self.lbl = QLabel(self)
        self.lbl.resize(300,300)
        pixmap = QPixmap(file_addr)
        self.lbl.setPixmap(pixmap)
        self.lbl.resize(300,300)
        self.lbl.setGeometry(150,400,300,300)
        self.lbl.show()

    def close_image(self):
        try:
            self.lbl.hide()
        except:
            pass



if __name__ == "__main__":
    #initialize

    app = QApplication(sys.argv)
    #gui = TestGui()
    main_ui = mapping_ui()
    main_ui.show()


   # gui.show()
   # gui.open_image(gui.get_map_addr())
    
    
    app.exec_()


# Create window
#app = QApplication(sys.argv)
#w = QWidget()
#w.setWindowTitle("Mapping Mode ")

# Create widget
#label = QLabel(w)
#pixmap = QPixmap('./gui/grid_map.jpg')
#label.setPixmap(pixmap)
#w.resize(pixmap.width(),pixmap.height())

# Draw window
#w.show()

#불러온 사진파일별로 다르게 목적지 저장하기 ? 그럴 필요는 없을듯
#한글로 목적지명 저장하기
