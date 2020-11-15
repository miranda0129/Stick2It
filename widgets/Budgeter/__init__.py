from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, QPushButton, QTextEdit, QListWidget
from PyQt5.QtCore import QSize
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from widgets import global_vars as gv

qtcreator_file = "widgets/Budgeter/budgeter.ui"  # Enter file here.


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        # name widget for window management
        self.name = "widget3"

        # load ui file
        QtWidgets.QMainWindow.__init__(self)
        uic.loadUi(qtcreator_file, self)
        self.show()

    # close event will update global var tracking open widgets
    def closeEvent(self, event):
        print("closing window...")
        print(gv.open_widgets)
        del gv.open_widgets[self.name]
        print(gv.open_widgets)