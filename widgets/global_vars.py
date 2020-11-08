from widgets import TestWidget
from widgets import ToDoList

"""
a dictionary of Stick2It widget objectNames and their associated QT widget class
"""
widget_dict = {
    "widget1": ToDoList.Window
}

"""
open_widgets: a dictionary of open widgets, using the above formulation, but with objects instead of classes
"""
open_widgets = {}