import unittest
import time

# os changes to make python think it is in the above directory
import os
os.chdir("../")
import sys
sys.path.append("./")

from widgets import global_vars as gv
from widgets import app
from PyQt5.QtTest import QTest, QSignalSpy
from PyQt5.QtCore import Qt, QThread

new_app, window = app.run()

class TimerTest(unittest.TestCase):
    # open widget
    def test_case1(self):
        print("test setup")
        QTest.mouseClick(window.widget4, Qt.LeftButton)
        print(f"current window: {gv.current_window}")
        QTest.mouseClick(gv.current_window, Qt.LeftButton)

    # create 4 or 5 sample timers
    def test_case2(self):
        print("test timers")
        gv.current_window.timerEdit.setText("00:01")

    # start and stop them at different intervals
    def test_case3(self):
        print("test start stop")
        QTest.mouseClick(gv.current_window.startButton, Qt.LeftButton)
        spy = QSignalSpy(gv.current_window.notify)
        print(f"Spy signal: {spy.wait(timeout=10000)}")

    # look for done popup
    def test_case4(self):
        self.assertTrue(gv.current_window.statusLabel.isVisible())

    # create a new file
    # save it and exit

if __name__ == "__main__":
    unittest.main()