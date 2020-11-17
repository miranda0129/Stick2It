from PyQt5.QtCore import QSize, QObject, pyqtSignal, QThread
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from widgets import global_vars as gv
from widgets.Timer.timer import Timer 

qtcreator_file = "widgets/Timer/timer.ui"  # Enter file here.
Ui_TimerWindow, QtBaseClass = uic.loadUiType(qtcreator_file)

import time

class Timer(QObject):
    finished = pyqtSignal()     # dont put this in __init__, it has to be outside

    def __init__(self, parent=None, window=None):
        if window:
            self.window = window 
        QObject.__init__(self, parent=parent)
        self.continue_run = True
    
    def countdown(self):
        print("starting countdown...")
        if not self.window.timerEdit:
            print("no timerEdit... please add it.")
        t = self.strToSec(self.window.timerEdit.text())
        while t != 0 and self.continue_run:
            mins, secs = divmod(t, 60)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            self.window.timerEdit.setText(timeformat)
            QThread.sleep(1)
            t -= 1
        print(t)
        if t == 0:
            print("countdown done!")
            self.window.timerEdit.setText("00:00")
            self.window.notify("done!")
        self.continue_run = True
        self.window.runningTimer = False
        self.finished.emit()

    def strToSec(self, s):
        mins = s[:2]
        secs = s[3:]
        return int(mins) * 60 + int(secs)
    
    def stop(self):
        print("stopping timer...")
        self.continue_run = False
    


class Window(QtWidgets.QMainWindow, Ui_TimerWindow):
    stop_signal = pyqtSignal()      # dont put this in __init__, it has to be outside
    def __init__(self):
        # name widget for window management
        self.name = "widget4"
        self.runningTimer = False

        # load and set up ui file
        QtWidgets.QMainWindow.__init__(self)
        Ui_TimerWindow.__init__(self)
        self.setupUi(self)
        self.statusLabel.hide()
        self.startButton.clicked.connect(self.timerInit)

    # code is bad and I should feel bad, multiple thread spawns
    # fix this when time persists
    def timerInit(self):
        self.statusLabel.hide()
        if not self.runningTimer:
            self.runningTimer = True
            # Thread:
            self.thread = QThread()
            self.timer = Timer(window = self)
            self.stop_signal.connect(self.timer.stop)  # connect stop signal to worker stop method
            self.timer.moveToThread(self.thread)

            self.timer.finished.connect(self.thread.quit)  # connect the workers finished signal to stop thread
            self.timer.finished.connect(self.timer.deleteLater)  # connect the workers finished signal to clean up worker
            self.thread.finished.connect(self.thread.deleteLater)  # connect threads finished signal to clean up thread

            self.thread.started.connect(self.timer.countdown)
            self.thread.finished.connect(self.timer.stop)

            # Start Button action:
            self.thread.start()

            # Stop Button action:
            self.stopButton.clicked.connect(self.stop_timer)
        
    def stop_timer(self):
        self.stop_signal.emit()
    

    # close event will update global var tracking open widgets
    def closeEvent(self, event):
        print("closing window...")
        print(gv.open_widgets)
        del gv.open_widgets[self.name]
        print(gv.open_widgets)
        
    def notify(self, text):
        print(f"sending {text} to client...")
        self.statusLabel.show()