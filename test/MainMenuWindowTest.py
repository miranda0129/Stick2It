import unittest

from PyQt5 import QtWidgets
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt


from widgets.MainMenu import MainMenuWindow

app = QtWidgets.QApplication([])


class MyTestCase(unittest.TestCase):

    def setUp(self):
        '''Create the GUI'''
        self.form = MainMenuWindow()

    def test_app(self):
        for button in self.form.widgetButtons.findChildren(QtWidgets.QPushButton):
            QTest.mouseClick(button, Qt.LeftButton)


if __name__ == '__main__':
    unittest.main()
