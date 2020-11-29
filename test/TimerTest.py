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
        try:
            print("test setup")
            QTest.mouseClick(window.widget4, Qt.LeftButton)
            print(f"current window: {gv.window}")
            QTest.mouseClick(gv.window, Qt.LeftButton)
        except Exception as e:
            self.fail(e)

    # create 4 or 5 sample timers
    def test_case2(self):
        try:
            tl = gv.window.timesLayout
            for i in range(tl.count()):
                t = tl.itemAt(i).widget()
                t.setText("00:01")
            print("test timers")
        except Exception as e:
            self.fail(e)


    # start and stop them at different intervals
    def test_case3(self):
        try:
            QTest.mouseClick(gv.window.toggleButton, Qt.LeftButton)
            spy = QSignalSpy(gv.window.notify)
            t = spy.wait(timeout=10000)
            print(f"Spy signal: {t}")
        except Exception as e:
            self.fail(e)

    # look for done popup
    def test_case4(self):
        self.assertTrue(gv.window.statusLabel.isVisible())

    # create a new file
    # save it and exit
    def test_case6(self):
        gv.window.close()
        window.close()

if __name__ == "__main__":
    unittest.main()