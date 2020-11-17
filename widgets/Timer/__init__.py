from PyQt5.QtCore import QSize
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from widgets import global_vars as gv

qtcreator_file = "widgets/Timer/timer.ui"  # Enter file here.
Ui_TimerWindow, QtBaseClass = uic.loadUiType(qtcreator_file)

class Window(QtWidgets.QMainWindow, Ui_TimerWindow):
    def __init__(self):
        # name widget for window management
        self.name = "widget4"

        # load and set up ui file
        QtWidgets.QMainWindow.__init__(self)
        Ui_TimerWindow.__init__(self)
        self.setupUi(self)

        # yea, dynamic resizing would be better, but for now this will do. Lots of room, will fit exactly how I make the qt design
        self.setFixedSize(615, 600)

    # close event will update global var tracking open widgets
    def closeEvent(self, event):
        print("closing window...")
        print(gv.open_widgets)
        del gv.open_widgets[self.name]
        print(gv.open_widgets)