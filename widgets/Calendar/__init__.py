from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget
from PyQt5.QtCore import QSize    
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from widgets import global_vars as gv


qtcreator_file  = "widgets/Calendar/Calendar.ui" # Enter file here.
Ui_CalendarWindow, QtBaseClass = uic.loadUiType(qtcreator_file)

class Window(QtWidgets.QMainWindow, Ui_CalendarWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_CalendarWindow.__init__(self)
        self.setupUi(self)
        self.name = "widget2"

    def closeEvent(self, event):
        print("closing window...")
        print(gv.open_widgets)
        del gv.open_widgets[self.name]
        print(gv.open_widgets)
