from PyQt5 import QtCore, QtGui, QtWidgets, uic
from widgets import global_vars as gv

qtcreator_file  = "widgets/MainMenu/design.ui" # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtcreator_file)

class MainMenuWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def load_widget(self):
        button = self.sender()
        name = button.objectName()
        app = gv.widget_dict[name]()
        print(f"loading app: {app}")
        if app: app.show()
        gv.open_widgets[name] = app
        # for testing
        gv.window = app
        # print("Error in Widget. Check error message. ")
        # print(e)


    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.openWidgets = []

        for button in self.widgetButtons.findChildren(QtWidgets.QPushButton):
            button.clicked.connect(self.load_widget) # Simulates pushing every widget button

            # for any button clicked, try to load the widget
    
    def closeEvent(self, event):
        if not gv.open_widgets:
            print("exiting...")
            import sys
            sys.exit()