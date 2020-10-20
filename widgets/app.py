from PyQt5 import QtWidgets
from widgets.MainMenu import MainMenuWindow

"""

Stick2it widgets: a lot of small productivity apps

The main menu is the default widget that is loaded. Other widgets that will be loaded are located in folders within. 

each widget has:
 - a design folder (with .ui or .qml designs)
 - app.py for the main app class (the window)
"""

def run():
    app = QtWidgets.QApplication([])
    window = MainMenuWindow()
    window.show()
    app.exec_()