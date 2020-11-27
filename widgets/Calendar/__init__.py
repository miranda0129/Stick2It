from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QDateEdit, QCalendarWidget, QPushButton, QLabel, QMainWindow
from PyQt5.QtCore import QSize    
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from widgets import global_vars as gv

qtcreator_file  = "widgets/Calendar/Calendar.ui" # Enter file here.
Ui_CalendarWindow, QtBaseClass = uic.loadUiType(qtcreator_file)

class Window(QtWidgets.QMainWindow, Ui_CalendarWindow):
    #test = True
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_CalendarWindow.__init__(self)
        self.setupUi(self)
        
        self.name = "widget2"
        self.date1 = self.findChild(QDateEdit, "dateEdit")
        self.cal = self.findChild(QCalendarWidget, "calendarWidget")

        self.calcButton = self.findChild(QPushButton, "pushButton")
        self.display = self.findChild(QLabel, "label")

        self.calcButton.clicked.connect(self.howFarDate)
  
        self.currentDay = self.cal.selectedDate().day()
        self.currentMonth = self.cal.selectedDate().month()
        self.currentYear = self.cal.selectedDate().year()

        self.cal.selectionChanged.connect(self.calDateChanged)
        self.date1.dateChanged.connect(self.dateEditChanged)

    def calDateChanged(self):
        self.date1.setDate(self.cal.selectedDate())
        test1 = self.cal.selectedDate().toString()

    def dateEditChanged(self):
        self.cal.setSelectedDate(self.date1.date())
        return (self.date1.date())
    
    def howFarDate(self):
     
        day = self.cal.selectedDate().day()
        month = self.cal.selectedDate().month()
        year = self.cal.selectedDate().year()
        distance = 0

        #Calculate the difference in days for the years! accounts for leap years
        a = year - self.currentYear
        if(a < 0):
            for i in range(year, self.currentYear):
                if(i%4 == 0):
                    distance -= 366
                else:
                    distance -= 365
        if(a > 0):
            for i in range(self.currentYear, self.Year):
                if(i%4 == 0):
                    distance += 366
                else:
                    distance += 365

        #Calculate the difference in days based off the months!
        b = month - self.currentMonth
        if(b < 0):
            for i in range(month, self.currentMonth):
                if(i in [1,3,5,7,8,10,12]):
                    distance -= 31
                elif(i == 2):
                    distance -= 28
                else:
                    distance -= 30
        if(b > 0):
            for i in range(self.currentMonth, month):
                if(i in [1,3,5,7,8,10,12]):
                    distance += 31
                elif(i == 2):
                    distance += 28
                else:
                    distance += 30

        #Days are the easiest, just find the difference
        distance += day - self.currentDay

        #Display an appropriate message based on how far the date is
        if(distance > 0):
            self.display.setText(str(distance) + " day(s) away!")
        elif(distance <0):
            self.display.setText(str(abs(distance)) + " day(s) ago!")
        else:
            self.display.setText("Thats Today!")
            
        
    def closeEvent(self, event):
        print("closing window...")
        print(gv.open_widgets)
        del gv.open_widgets[self.name]
        print(gv.open_widgets)
