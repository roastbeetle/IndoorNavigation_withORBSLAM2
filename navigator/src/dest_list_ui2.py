#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dest_list.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(object):
    def setupUi(self, Form, dest_list):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(597, 1024)
        Form.setStyleSheet(_fromUtf8("background-color:rgb(250, 250, 250)"))
        self.pushButton = QtGui.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(195, 920, 210, 80))
        self.pushButton.setStyleSheet(_fromUtf8("background-color:rgb(42, 42, 42);\n"
"font: 28pt \"맑은 고딕\";\n"
"color:rgb(255,255,255);\n"
"border-radius: 10px;"))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_4 = QtGui.QPushButton(Form)
        self.pushButton_4.setGeometry(QtCore.QRect(75, 490, 450, 120))
        self.pushButton_4.setStyleSheet(_fromUtf8("background-color: rgb(70, 125, 255);\n"
"color: rgb(255,255,255);\n"
"border:none;\n"
"font: 48pt \"맑은 고딕\";\n"
"border-radius:10px;"))
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.pushButton_5 = QtGui.QPushButton(Form)
        self.pushButton_5.setGeometry(QtCore.QRect(75, 680, 450, 120))
        self.pushButton_5.setStyleSheet(_fromUtf8("background-color: rgb(70, 125, 255);\n"
"color: rgb(255,255,255);\n"
"border:none;\n"
"font: 48pt \"맑은 고딕\";\n"
"border-radius:10px;"))
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))
        self.pushButton_6 = QtGui.QPushButton(Form)
        self.pushButton_6.setGeometry(QtCore.QRect(75, 110, 450, 120))
        self.pushButton_6.setStyleSheet(_fromUtf8("background-color: rgb(70, 125, 255);\n"
"color: rgb(255,255,255);\n"
"border:none;\n"
"font: 48pt \"맑은 고딕\";\n"
"border-radius:10px;"))
        self.pushButton_6.setObjectName(_fromUtf8("pushButton_6"))
        self.pushButton_7 = QtGui.QPushButton(Form)
        self.pushButton_7.setGeometry(QtCore.QRect(75, 300, 450, 120))
        self.pushButton_7.setStyleSheet(_fromUtf8("background-color: rgb(70, 125, 255);\n"
"color: rgb(255,255,255);\n"
"border:none;\n"
"font: 48pt \"맑은 고딕\";\n"
"border-radius:10px;"))
        self.pushButton_7.setObjectName(_fromUtf8("pushButton_7"))

        self.retranslateUi(Form, dest_list)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Form.home)
        QtCore.QObject.connect(self.pushButton_4, QtCore.SIGNAL(_fromUtf8("clicked()")), Form.btn1)
        QtCore.QObject.connect(self.pushButton_5, QtCore.SIGNAL(_fromUtf8("clicked()")), Form.btn2)
        QtCore.QObject.connect(self.pushButton_6, QtCore.SIGNAL(_fromUtf8("clicked()")), Form.btn3)
        QtCore.QObject.connect(self.pushButton_7, QtCore.SIGNAL(_fromUtf8("clicked()")), Form.btn4)
        #self.pushButtonx = QtGui.QPushButton(Form)
        #QtCore.QObject.connect(self.pushButtonx, QtCore.SIGNAL("do_update"), Form.update)

        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form, dest_list):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.pushButton.setText(_translate("Form", "Home", None))
        self.pushButton_4.setText(_translate("Form", dest_list[0][0], None))
        self.pushButton_5.setText(_translate("Form", dest_list[1][0], None))
        self.pushButton_6.setText(_translate("Form", dest_list[2][0], None))
        self.pushButton_7.setText(_translate("Form", dest_list[3][0], None))
#
#if __name__ == "__main__":
#    import sys
#    app = QtGui.QApplication(sys.argv)
#    form = QtGui.QWidget()
#    ui = Ui_Form()
#    ui.setupUi(form)
#    form.show()
#    sys.exit(app.exec_())

