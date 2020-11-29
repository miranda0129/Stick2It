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
            self.window.timerEdit.setText("00:00")
            QThread.sleep(1)
            print("countdown done!")
            self.window.done.emit("done")

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

#TODO: more than one time for a timer (ex: 25/5 pomodoro, 20/0.2 eye strain, etc.)
"""
class Window(QtWidgets.QMainWindow, Ui_TimerWindow):
    done = pyqtSignal(str)
    def __init__(self):
        # load and set up ui file
        QtWidgets.QMainWindow.__init__(self)
        Ui_TimerWindow.__init__(self)
        self.setupUi(self)
        self.statusLabel.hide()

        # name widget for window management
        self.name = "widget4"
        self.load_timers()

        # notification signal toggler
        self.done.connect(self.check_if_done)
        # TODO: start/stop toggler instead of separate buttons
        self.timerEdit.returnPressed.connect(self.start_timer)  # enter key triggers start
        self.toggleButton.clicked.connect(self.start_stop_toggler)
        self.addTimer.clicked.connect(self.add_timer)
        self.addTime.clicked.connect(lambda: self.add_time("05:00", False))
    
    # quick way to get timer
    def timer(self):
        return self.timers[self.index]

    """
        load_timers: if a time file exists, then load it up at startup. If not, then be a blank startup. 
    """
    def load_timers(self):
        self.timers = []            # an array of Timer objects, with an associated button
        self.index = -1             # which Timer of the array is loaded into the widget
        self.timer_t = None         # timer thread, which begins a countdown
        self.timer_t_started = False     # too lazy to figure out how PyQT can check for deleted C++ objects

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
        print(timer)
        self.timers.append(timer)
        print("timers: " + str(self.timers))
        btn = QtWidgets.QPushButton(timer.name)
        btn.clicked.connect(self.init_timer)
        btn.setCheckable(True)
        self.timerLayout.addWidget(btn)
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
            new_timer = self.timers[new_index]
            if self.index != -1:
                # replace self.index with current timer time (and name)
                old_timer = self.timer()
                #print(f"old timer: {old_timer}")
                #print(f"new timer: {new_timer}")
                print("times: " + str(self.timers))
                #old_timer.times = [self.timerEdit.text()]
                for i in range(self.timesLayout.count()):
                    self.timesLayout.itemAt(i).widget().deleteLater()

            # move to new_index
            for time in new_timer.times:
                self.add_time(time, True)
            self.timerEdit.setText(new_timer.times[0])
            self.index = new_index
   
    # used in connections
    def toggle_timer_t(self):
        self.timer_t_started = not self.timer_t_started

    """
        boolean to toggle starting and stopping
            True: change text of button to stop, in countdown state
            False: change text of button to start, in edit state
    """
    def start_stop_toggler(self):
        if not self.timer_t_started:
            self.lock_edited_times()
            self.switch_time(0)
            self.start_timer()
            self.toggleButton.setText("Stop")
        else:
            self.stop_timer()

    def start_timer(self):
        if not self.timer_t_started:
            self.statusLabel.hide()
            self.timer_t = TimerThread(window=self)
            self.timer_t.finished.connect(self.timer_t.quit)  # connect the workers finished signal to stop thread
            self.timer_t.finished.connect(self.timer_t.deleteLater)  # connect the workers finished signal to stop thread
            self.timer_t.finished.connect(self.toggle_timer_t)
            self.timer_t.start()
            self.toggle_timer_t()
    
    def stop_timer(self):
        if self.timer_t_started:
            self.switch_time(-1)
            self.timer_t.stop_signal.emit()
    
    """
    add_time: initializes the time onto the window
              if not in_timer, then also add it to the current timer array in memory. 
    """
    def add_time(self, time, in_timer):
        if self.timers:
            if not in_timer:
                self.timer().times.append(time)
                print("times: " + str(self.timers))
            line = QtWidgets.QLineEdit(time)
            line.setMaximumWidth(100)
            line.setMinimumHeight(30)
            line.setAlignment(QtCore.Qt.AlignCenter)
            line.setInputMask("00:00")
            # line.setStyleSheet("border: 0;")
            self.timesLayout.addWidget(line)
            print(self.timesLayout.itemAt(0))
            print(f"time: {time}")
    
    # switches the time on screen to the specified index
    def switch_time(self, index):
        if index != -1:
            time = self.timer().times[index]
            # switch timer on screen
            self.timerEdit.setText(time)
            # color current timer
            self.timesLayout.itemAt(index).widget().setStyleSheet("background-color: yellow;")
            # remove previous color (if not start)
            if index != 0:
                self.timesLayout.itemAt(self.timer().index - 1).widget().setStyleSheet("")
        else:
            self.timesLayout.itemAt(self.timer().index).widget().setStyleSheet("")
            self.timer().index = 0
            time = self.timer().times[0]
            self.timerEdit.setText(time)
            self.toggleButton.setText("Start")
            self.toggle_timer_t()
    
    def lock_edited_times(self):
        for i in range(self.timesLayout.count()):
            self.timer().times[i] = self.timesLayout.itemAt(i).widget().text()
        print(self.timer())

 
    # close event will update global var tracking open widgets
    def closeEvent(self, event):
        print("closing window...")
        print(gv.open_widgets)
        del gv.open_widgets[self.name]
        print(gv.open_widgets)
        
    def check_if_done(self, text):
        if self.timer().index != len(self.timer().times) - 1:
            print("not done yet!")
            self.timer().index += 1
            self.switch_time(self.timer().index)
            self.toggle_timer_t()
            self.start_timer()
        else:
            print("finally done!")
            # timer is done. move to first time and notify
            self.switch_time(-1)
            self.notify(text)


    def notify(self, text):
        print(f"sending {text} to client...")
        self.statusLabel.show()