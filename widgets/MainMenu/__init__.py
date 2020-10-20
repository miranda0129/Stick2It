from PyQt5 import QtCore, QtGui, QtWidgets, uic

qtcreator_file  = "widgets/MainMenu/design.ui" # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtcreator_file)


class MainMenuWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def loadWidget(self):
        button = self.sender()
        name = button.objectName()
        print(name)
        

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        for button in self.widgetButtons.findChildren(QtWidgets.QPushButton):
            button.clicked.connect(self.loadWidget)