# Objects for the timer widget

"""
timer object has:

- times (dynamic list of times to iterate)
- name (string)

"""

class Timer:
    def __init__(self, time=None, name=None):
        if time:
            self.time = time        # list of time strings of the form NN:NN, that go in succession
        else:
            self.time = "00:10"
        if name:
            self.name = name        # name assigned to the timer
        else:
            self.name = "timer"