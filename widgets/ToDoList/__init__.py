from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, QPushButton, QTextEdit, QListWidget
from PyQt5.QtCore import QSize    
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from widgets import global_vars as gv

qtcreator_file  = "widgets/ToDoList/toDoList.ui" # Enter file here.

class Window(QtWidgets.QMainWindow):
    def __init__(self): 
        #name widget for window management
        self.name = "widget1"

        #load ui file
        QtWidgets.QMainWindow.__init__(self)
        uic.loadUi(qtcreator_file, self)
        self.show()

        #get object pointers
        self.addButton = self.findChild(QPushButton, "addItemButton")
        self.deleteButton = self.findChild(QPushButton, "deleteItemButton")
        self.newInputItem = self.findChild(QTextEdit, "newItemInput")
        self.list = self.findChild(QListWidget, "list")

        self.loadList();
        
        #call addItem handler when clicked
        self.addButton.clicked.connect(self.clickedAddBtn)

        #call deleteItem handler when clicked
        self.deleteButton.clicked.connect(self.clickedDelBtn)

    #add item button handler (adds newItemInput to list)
    def clickedAddBtn(self):
        newItem = self.newInputItem.toPlainText() + "\n"
        self.list.addItem(newItem)
        self.newInputItem.setPlainText("")
   
   #delete item button handler (deleted selected item from list)
    def clickedDelBtn(self):
        selected = self.list.selectedIndexes()

        for item in selected:
            index = item.row()
            self.list.takeItem(index)

    #close event will update gobal var tracking open widgets
    #will also save current list to file
    def closeEvent(self, event):
        #will overwrite current file contents
        SavedList = open("SavedList.txt", "w")
        #starts at end of list prints text to file while more rows
        rows = self.list.count()
        current = 0
        while current < rows:
            text = self.list.item(current).text()
            SavedList.write(text)
            current += 1
        SavedList.close()

        print("closing window...")
        print(gv.open_widgets)
        del gv.open_widgets[self.name]
        print(gv.open_widgets)

    def loadList(self):
        SavedList = open("SavedList.txt", "r")
        Items = SavedList.readlines()
        SavedList.close()
        for newItem in Items:
            self.list.addItem(newItem)
            