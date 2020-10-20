from PyQt5 import QtCore, QtGui, QtWidgets, uic
from widgets import global_vars as gv

qtcreator_file  = "widgets/MainMenu/design.ui" # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtcreator_file)

class MainMenuWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def load_widget(self):
        button = self.sender()
        name = button.objectName()
        try:
            app = gv.widget_dict[name]()
            if app: app.show()
            gv.open_widgets[name] = app
        except:
            print("no widget implemented yet...")

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.openWidgets = []

        for button in self.widgetButtons.findChildren(QtWidgets.QPushButton):
            button.clicked.connect(self.load_widget)