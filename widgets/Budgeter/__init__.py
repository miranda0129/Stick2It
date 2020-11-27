from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, QPushButton, QTextEdit, QListWidget
from PyQt5.QtCore import QSize
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from widgets import global_vars as gv

qtcreator_file = "widgets/Budgeter/budgeter.ui"  # Enter file here.
Ui_BudgetWindow, QtBaseClass = uic.loadUiType(qtcreator_file)


class Window(QtWidgets.QMainWindow, Ui_BudgetWindow):
    def __init__(self):
        # name widget for window management
        self.name = "widget3"

        # load and set up ui file
        QtWidgets.QMainWindow.__init__(self)
        Ui_BudgetWindow.__init__(self)
        self.setupUi(self)

        # connect budgetButton to function when clicked
        self.budgetButton.clicked.connect(self.calculateBudget)

        # connect summaryButton to function when clicked
        self.summaryButton.clicked.connect(self.calculateSummary)

    def calculateBudget(self):
        temp_costs = self.fixedCost.text().replace(' ', '')
        temp_income = self.expectedIncome.text().replace(' ', '')
        temp_savings = self.savings.text().replace(' ', '')

        if len(temp_costs) > 0:
            costs = temp_costs.split(",")
            # returns sum of the fixed costs, accepts list of numbers or name: value pairs
            total_cost = sum([float(cost.split(":")[-1]) for cost in costs])
        else:
            total_cost = 0

        if len(temp_income) > 0:
            incomes = temp_income.split(",")
            total_income = sum([float(income.split(":")[-1]) for income in incomes])
        else:
            total_income = 0

        if len(temp_savings) > 0:
            savings = temp_savings
        else:
            savings = "0"

        if savings[-1] == '%':  # case where saving is a percent of income
            percentage = float(savings.replace('%', '')) / 100
            saved = percentage * total_income
        else:
            saved = float(savings)

        spending = total_income - saved - total_cost

        spending_str = "${:.2f}".format(spending)
        self.result.setText(spending_str)

    # close event will update global var tracking open widgets

    def calculateSummary(self):

        temp_costs = self.fixedCost.text().replace(' ', '')
        temp_income = self.expectedIncome.text().replace(' ', '')
        temp_savings = self.savings.text().replace(' ', '')

        if len(temp_costs) > 0:
            costs = temp_costs.split(",")
            # returns sum of the fixed costs, accepts list of numbers or name: value pairs
            total_cost = sum([float(cost.split(":")[-1]) for cost in costs])
        else:
            total_cost = 0

        if len(temp_income) > 0:
            incomes = temp_income.split(",")
            total_income = sum([float(income.split(":")[-1]) for income in incomes])
        else:
            total_income = 0

        if len(temp_savings) > 0:
            savings = temp_savings
        else:
            savings = "0"

        if savings[-1] == '%':  # case where saving is a percent of income
            percentage = float(savings.replace('%', '')) / 100
            saved = percentage * total_income
        else:
            saved = float(savings)

        summary_str = "Total Income: ${:.2f}, Total Cost: ${:.2f}".format(total_income, total_cost)
        self.summary.setText(summary_str)

    def closeEvent(self, event):
        print("closing window...")
        print(gv.open_widgets)
        del gv.open_widgets[self.name]
        print(gv.open_widgets)
