from PyQt5.QtCore import QSize, QObject, pyqtSignal, QThread
from PyQt5 import QtCore, QtGui, uic
from PyQt5.QtWidgets import *
from widgets import global_vars as gv
from widgets.Timer.objects import Timer
import os.path
from pynotifier import Notification

qtcreator_file = "widgets/Timer/timer.ui"  # Enter file here.
Ui_TimerWindow, QtBaseClass = uic.loadUiType(qtcreator_file)

from datetime import datetime
import time

"""
TimerThread: creates a specific QThread that counts down a time. 
"""
class TimerThread(QThread):
    stop_signal = pyqtSignal()     # dont put this in __init__, it has to be outside

    def __init__(self, window=None):
        QThread.__init__(self)
        self.stop_signal.connect(self.stop)
        if window is not None:
            self.window = window 
    
    def run(self):
        print("starting countdown...")
        s = Timer.strToSec(self.window.timerEdit.text())
        t = s
        t2 = t

        self.continue_run = True
        start_time = datetime.now()
        while t != 0 and self.continue_run:
            if t != t2: 
                print("timer still running...")
                t = t2
                mins, secs = divmod(t, 60)
                timeformat = '{:02d}:{:02d}'.format(mins, secs)
                self.window.timerEdit.setText(timeformat)
                QThread.usleep(20)
            t2 = s - (datetime.now() - start_time).seconds
        if t == 0:
            self.window.timerEdit.setText("00:00")
            QThread.sleep(1)
            print("countdown done!")
            self.window.done.emit()
        else:
            print("stopped timer")

    def stop(self):
        print("stopping timer...")
        self.continue_run = False

"""
Window acts as the GUI and the controller. It will control starting and stopping a specific time, as well as
managing different timers stored as a list of timer objects

#TODO: more than one time for a timer (ex: 25/5 pomodoro, 20/0.2 eye strain, etc.)
"""
class Window(QMainWindow, Ui_TimerWindow):
    done = pyqtSignal()
    notify = pyqtSignal(str)
    def __init__(self):
        # load and set up ui file
        QMainWindow.__init__(self)
        Ui_TimerWindow.__init__(self)
        self.setupUi(self)
        self.statusLabel.hide()
        self.actionNew.triggered.connect(self.new_file)
        self.actionOpen.triggered.connect(self.open_file)
        self.actionSave.triggered.connect(self.save_file)
        self.actionSave_As.triggered.connect(self.save_file_as)

        # name widget for window management
        self.name = "widget4"
        self.load_timers()

        # notification signal toggler
        self.done.connect(self.check_if_done)
        self.notify.connect(self.notify_handler)

        # TODO: start/stop toggler instead of separate buttons
        self.timerEdit.returnPressed.connect(self.start_timer)  # enter key triggers start
        self.toggleButton.clicked.connect(self.start_stop_toggler)
        self.addTimer.clicked.connect(self.add_timer)
        self.delTimer.clicked.connect(self.del_timer)
        self.addTime.clicked.connect(lambda: self.add_time("05:00", False))
        self.delTime.clicked.connect(self.del_time)
    
    # quick way to get timer
    def timer(self):
        return self.timers[self.index]

    """
        load_timers: if a time file exists, then load it up at startup. If not, then be a blank startup. 
    """
    def load_timers(self, file='widgets/Timer/data/timer1.json'):
        self.timers = []            # an array of Timer objects, with an associated button
        self.index = -1             # which Timer of the array is loaded into the widget
        self.timer_t = None         # timer thread, which begins a countdown
        self.timer_t_started = False     # too lazy to figure out how PyQT can check for deleted C++ objects
        self.offset = 0             # to fix deletion clashing

        self.btnGroup = QButtonGroup()
        self.btnGroup.setExclusive(True)
        if file and os.path.isfile(file):
            print("file exists. Loading file. ")
        else:
            print("file does not exist. Creating default timer file. ")
            self.add_timer(is_checked=True)
    
    def add_timer(self, is_checked=False):
        timer = Timer(name=f"timer {len(self.timers) + self.offset}")
        print(timer)
        self.timers.append(timer)
        print("timers: " + str(self.timers))
        btn = EditButton(timer.name)
        btn.clicked.connect(self.init_timer)
        btn.setCheckable(True)
        self.timerLayout.addWidget(btn)
        self.btnGroup.addButton(btn, len(self.timers) - 1 + self.offset)
        if is_checked:
            btn.setChecked(True)
            self.init_timer()
    
    # deletes the selected timer (at the selected index)
    def del_timer(self):
        if len(self.timers) > 1:
            i = 0
            if self.index == 0:
                i = 1
            if self.index != len(self.timers) - 1:
                self.offset += 1
            j = self.index
            self.timerLayout.itemAt(i).widget().setChecked(True)
            self.init_timer()
            print(f"deleting timer at index {j}")
            item = self.timerLayout.itemAt(j)
            self.timerLayout.removeItem(item)
            self.btnGroup.removeButton(item.widget())
            item.widget().deleteLater()
            self.timers.pop(j)



        
    """
        init_timer: after a button toggle is toggled on, run this function.
            it uses the QButton's associated ID in the QButtonGroup, and
            opens the associated button in the self.timers list. 

            it also replaces current timer data in the old index at self.index.  
    """
    def init_timer(self):
        # dont initialize the timer if there is a timer running
        if self.timer_t_started:
            self.timerLayout.itemAt(self.index).widget().setChecked(True)
            return
        new_index = self.timerLayout.indexOf(self.btnGroup.checkedButton())
        print(f"new index: {new_index}")
        if new_index != -1:
            if self.index == new_index: 
                # do nothing
                return
            new_timer = self.timers[new_index]
            print("timers: " + str(self.timers))
            if self.index != -1:
                # replace self.index with current timer time (and name)
                old_timer = self.timer()
                #print(f"old timer: {old_timer}")
                #print(f"new timer: {new_timer}")
                #old_timer.times = [self.timerEdit.text()]
                self.lock_edited_times()
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
        print(self.timer_t_started)

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
            line = QLineEdit(time)
            line.setMaximumWidth(100)
            line.setMinimumHeight(30)
            line.setAlignment(QtCore.Qt.AlignCenter)
            line.setInputMask("00:00")
            # line.setStyleSheet("border: 0;")
            self.timesLayout.addWidget(line)
            print(f"time: {time}")
    
    # deletes the selected time (at the selected index)
    def del_time(self):
        if len(self.timer().times) > 1:
            self.timer().times.pop()
            item = self.timesLayout.itemAt(self.timesLayout.count()-1)
            self.timesLayout.removeItem(item)
            item.widget().deleteLater()

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
        if self.timer_t:
            try:
                self.timer_t.stop_signal.emit()
            except:
                pass
        print("closing window...")
        print(gv.open_widgets)
        del gv.open_widgets[self.name]
        print(gv.open_widgets)

    
    def check_if_done(self):
        if self.timer().index != len(self.timer().times) - 1:
            print("not done yet!")
            self.timer().index += 1
            self.switch_time(self.timer().index)
            self.toggle_timer_t()
            self.start_timer()
            if Timer.strToSec(self.timer().time()) > 10:
                self.notify.emit(f"counting down timer {self.timer().time()}")
        else:
            print("finally done!")
            # timer is done. move to first time and notify
            self.switch_time(-1)
            self.notify.emit("done!")


    def notify_handler(self, text):
        print(f"sending {text} to client...")
        self.statusLabel.show()
        Notification(
            title=f'{self.timer().name}',
            description=f'{text}',
            #icon_path='path/to/image/file/icon.png', # On Windows .ico is required, on Linux - .png
            duration=5,                              # Duration in seconds
            urgency=Notification.URGENCY_CRITICAL
        ).send()
    

    #FILE SAVING
    def new_file(self):
        print("new file")


    def open_file(self):
        print("open file")
    
    def save_file(self):
        print("save file")
    
    def save_file_as(self):
        print("save file as")

    

"""
a button with an edit property when you double click it.
"""
class EditButton(QPushButton):
    def settings_dialog(self):
        text, ok = QInputDialog.getText(self, f"{self.text()} settings", 'timer name:', QLineEdit.Normal, self.text())
        if ok:
            i = self.window().timerLayout.indexOf(self)
            self.setText(text)
            self.window().timers[i].name = text

    def mouseDoubleClickEvent(self, event):
        self.settings_dialog()
    
    def eventFilter(self, QObject, event):
        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.RightButton:
                print("Right button clicked")
        return False
