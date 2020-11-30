from widgets import TestWidget, Budgeter, ToDoList, Calendar, Timer

"""
a dictionary of Stick2It widget objectNames and their associated QT widget class
"""
widget_dict = {
	"widget1": ToDoList.Window,
	"widget2": Calendar.Window,
	"widget3": Budgeter.Window,
	"widget4": Timer.Window
}

"""
open_widgets: a dictionary of open widgets, using the above formulation, but with objects instead of classes
"""
open_widgets = {}

# window: for testing
window = None