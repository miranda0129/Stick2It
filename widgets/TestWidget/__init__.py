from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget
from PyQt5.QtCore import QSize    
from widgets import global_vars as gv

class Window(QWidget):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Test Widget")
        #self.name = "widget1"

    def closeEvent(self, event):
        print("closing window...")
        print(gv.open_widgets)
        del gv.open_widgets[self.name]
        print(gv.open_widgets)