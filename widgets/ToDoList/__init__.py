from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget
from PyQt5.QtCore import QSize    
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from widgets import global_vars as gv


qtcreator_file  = "widgets/ToDoList/toDoList.ui" # Enter file here.
Ui_ToDoListWindow, QtBaseClass = uic.loadUiType(qtcreator_file)

class Window(QtWidgets.QMainWindow, Ui_ToDoListWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_ToDoListWindow.__init__(self)
        self.setupUi(self)
        self.name = "widget1"

    def closeEvent(self, event):
        print("closing window...")
        print(gv.open_widgets)
        del gv.open_widgets[self.name]
        print(gv.open_widgets)