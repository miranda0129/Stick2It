# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Calendar.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Calendar(object):
    def setupUi(self, Calendar):
        Calendar.setObjectName("Calendar")
        Calendar.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(Calendar)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setObjectName("gridLayout")
        self.calendarWidget = QtWidgets.QCalendarWidget(self.frame)
        self.calendarWidget.setObjectName("calendarWidget")
        self.gridLayout.addWidget(self.calendarWidget, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.frame, 0, 0, 1, 1)
        Calendar.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Calendar)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        Calendar.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Calendar)
        self.statusbar.setObjectName("statusbar")
        Calendar.setStatusBar(self.statusbar)

        self.retranslateUi(Calendar)
        QtCore.QMetaObject.connectSlotsByName(Calendar)

    def retranslateUi(self, Calendar):
        _translate = QtCore.QCoreApplication.translate
        Calendar.setWindowTitle(_translate("Calendar", "MainWindow"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Calendar = QtWidgets.QMainWindow()
    ui = Ui_Calendar()
    ui.setupUi(Calendar)
    Calendar.show()
    sys.exit(app.exec_())