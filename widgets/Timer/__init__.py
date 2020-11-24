from PyQt5.QtCore import QSize, QObject, pyqtSignal, QThread
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from widgets import global_vars as gv

qtcreator_file = "widgets/Timer/timer.ui"  # Enter file here.
Ui_TimerWindow, QtBaseClass = uic.loadUiType(qtcreator_file)

import time

class Timer(QThread):
    stop_signal = pyqtSignal()     # dont put this in __init__, it has to be outside

    def __init__(self, window=None):
        QThread.__init__(self)
        self.stop_signal.connect(self.stop)
        if window:
            self.window = window 
    
    def run(self):
        print("starting countdown...")
        if not self.window.timerEdit:
            print("no timerEdit... please add it.")
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

    def strToSec(self, s):
        mins = s[:2]
        secs = s[3:]
        return int(mins) * 60 + int(secs)
    
    def stop(self):
        print("stopping timer...")
        self.continue_run = False
    


class Window(QtWidgets.QMainWindow, Ui_TimerWindow):
    def __init__(self):
        # name widget for window management
        self.name = "widget4"

        # load and set up ui file
        QtWidgets.QMainWindow.__init__(self)
        Ui_TimerWindow.__init__(self)
        self.setupUi(self)
        self.statusLabel.hide()

        # Start Button action:
        self.startButton.clicked.connect(self.start_timer)

        # Stop Button action:
        self.stopButton.clicked.connect(self.stop_timer)

    def start_timer(self):
        self.statusLabel.hide()
        self.timer = Timer(window=self)
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