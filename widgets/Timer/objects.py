# Objects for the timer widget that are not a part of QT

"""
timer object has:

- times (dynamic list of times to iterate)
- name (string)
"""

class Timer:
    def __init__(self, times=None, name=None):
        if times is None:
            times=["25:00", "05:00"]
        if name is None:
            name="Default Timer"
        self.times = times        # list of time strings of the form NN:NN, that go in succession
        self.name = name        # name assigned to the timer
        self.index = 0          # where the timer is in the times array
    
    """
        for JSON storage, store the time and the name as strings
    """
    def to_dict(self):
        return {
            "times": self.times,
            "name": self.name
        }
    
    def __str__(self):
        return str(self.to_dict()) 

    def __repr__(self):
        return str(self.to_dict())
