from PyQt5.QtCore import QSize, QObject, pyqtSignal, QThread
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from widgets import global_vars as gv
import os.path

qtcreator_file = "widgets/Timer/timer.ui"  # Enter file here.
Ui_TimerWindow, QtBaseClass = uic.loadUiType(qtcreator_file)

import time

"""
TimerThread: creates a specific QThread that counts down from a Timer object. 
"""
class TimerThread(QThread):
    stop_signal = pyqtSignal()     # dont put this in __init__, it has to be outside

    def __init__(self, window=None):
        QThread.__init__(self)
        self.stop_signal.connect(self.stop)
        if window:
            self.window = window 
    
    def run(self):
        print("starting countdown...")
        t = self.strToSec(self.window.timerEdit.text())

        self.continue_run = True
        while t != 0 and self.continue_run:
            mins, secs = divmod(t, 60)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            self.window.timerEdit.setText(timeformat)
            QThread.sleep(1)
            t -= 1
        if t == 0:
            print("countdown done!")
            self.window.timerEdit.setText("00:00")
            self.window.notify("done!")

    """
    strToSec: converts a string of the form NN:NN to an integer representing number of seconds
    """
    def strToSec(self, s):
        mins = s[:2]
        secs = s[3:]
        min_sec = int(mins) * 60 + int(secs)
        return min_sec if min_sec <= 3600 else 3600
    
    def stop(self):
        print("stopping timer...")
        self.continue_run = False

"""
Window acts as the GUI and the controller. It will control starting and stopping a specific time, as well as
managing different timers stored as a list of timer objects

"""
class Window(QtWidgets.QMainWindow, Ui_TimerWindow):
    def __init__(self):
        # name widget for window management
        self.name = "widget4"

        # load and set up ui file
        QtWidgets.QMainWindow.__init__(self)
        Ui_TimerWindow.__init__(self)
        self.setupUi(self)
        self.statusLabel.hide()

        self.load_timers()

        self.startButton.clicked.connect(self.start_timer)
        self.stopButton.clicked.connect(self.stop_timer)
        self.addTimer.clicked.connect(self.add_timer)

    """
        load_timers: if a time file exists, then load it up at startup. If not, then be a blank startup. 
    """
    def load_timers(self):
        self.btnGroup = QtWidgets.QButtonGroup()
        self.btnGroup.setExclusive(True)
        default_file = 'widgets/Timer/data/timer1.json'
        if os.path.isfile(default_file):
            print("file exists. Loading file. ")
        else:
            print("file does not exist. Creating default timer file. ")
            self.add_timer(is_checked=True)
    
    def add_timer(self, is_checked=False):
        btn = QtWidgets.QPushButton("Default Timer")
        btn.setCheckable(True)
        if is_checked:
            btn.setChecked(True)
        self.timerHBox.addWidget(btn)
        self.btnGroup.addButton(btn)
        
    def start_timer(self):
        self.statusLabel.hide()
        self.timer = TimerThread(window=self)
        self.timer.finished.connect(self.timer.quit)  # connect the workers finished signal to stop thread
        self.timer.finished.connect(self.timer.deleteLater)  # connect the workers finished signal to stop thread
        self.timer.start()
    
    def stop_timer(self):
        self.timer.stop_signal.emit()

    # close event will update global var tracking open widgets
    def closeEvent(self, event):
        print("closing window...")
        print(gv.open_widgets)
        del gv.open_widgets[self.name]
        print(gv.open_widgets)
        
    def notify(self, text):
        print(f"sending {text} to client...")
        self.statusLabel.show()