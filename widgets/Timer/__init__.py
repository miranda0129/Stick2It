from PyQt5.QtCore import QSize, QObject, pyqtSignal, QThread
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from widgets import global_vars as gv
from widgets.Timer.objects import Timer
import os.path

qtcreator_file = "widgets/Timer/timer.ui"  # Enter file here.
Ui_TimerWindow, QtBaseClass = uic.loadUiType(qtcreator_file)

import time

"""
TimerThread: creates a specific QThread that counts down a time. 
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
        # load and set up ui file
        QtWidgets.QMainWindow.__init__(self)
        Ui_TimerWindow.__init__(self)
        self.setupUi(self)
        self.statusLabel.hide()

        # name widget for window management
        self.name = "widget4"
        self.load_timers()

        # TODO: start/stop toggler instead of separate buttons
        self.timerEdit.returnPressed.connect(self.start_timer)  # enter key triggers start
        self.startButton.clicked.connect(self.start_timer)
        self.stopButton.clicked.connect(self.stop_timer)
        self.addTimer.clicked.connect(self.add_timer)

    """
        load_timers: if a time file exists, then load it up at startup. If not, then be a blank startup. 
    """
    def load_timers(self):
        self.timers = []    # an array of Timer objects, with an associated button
        self.index = -1      # which Timer of the array is loaded into the widget

        self.btnGroup = QtWidgets.QButtonGroup()
        self.btnGroup.setExclusive(True)
        default_file = 'widgets/Timer/data/timer1.json'
        if os.path.isfile(default_file):
            print("file exists. Loading file. ")
        else:
            print("file does not exist. Creating default timer file. ")
            self.add_timer(is_checked=True)
    
    def add_timer(self, is_checked=False):
        timer = Timer(name=f"timer {len(self.timers)}")
        self.timers.append(timer)
        btn = QtWidgets.QPushButton(timer.name)
        btn.clicked.connect(self.init_timer)
        btn.setCheckable(True)
        self.timerHBox.addWidget(btn)
        self.btnGroup.addButton(btn, len(self.timers) - 1)
        if is_checked:
            btn.setChecked(True)
            self.init_timer()
        
    """
        init_timer: after a button toggle is toggled on, run this function.
            it uses the QButton's associated ID in the QButtonGroup, and
            opens the associated button in the self.timers list. 

            it also replaces current timer data in the old index at self.index.  
    """
    def init_timer(self):
        print("--------")
        new_index = self.btnGroup.checkedId()
        if new_index != -1:
            if self.index == new_index: 
                raise Exception("new timer index same as old timer index. An error has occured. ")
            
            # replace self.index with current timer time (and name)
            old_timer = self.timers[self.index]
            new_timer = self.timers[new_index]
            print(old_timer)
            print(new_timer)
            if self.index != -1:
                old_timer.times = [self.timerEdit.text()]

            print("--------")
            print(old_timer)
            print(new_timer)
            # move to new_index
            self.timerEdit.setText(new_timer.times[0])
            for i in range(len(new_timer.times)):
                print(f"time at index {i}: {new_timer.times[i]}")
            
            self.index = new_index

    """
        boolean to toggle starting and stopping
            True: change text of button to stop, in countdown state
            False: change text of button to start, in edit state
    """
    def start_stop_toggler(self):
        pass

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