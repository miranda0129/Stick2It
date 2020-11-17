import time

class Timer:
    def __init__(self, lineEdit=None):
        self.lineEdit = lineEdit
    def countdown(self, t):
        print("starting countdown...")
        while t:
            mins, secs = divmod(t, 60)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            if self.lineEdit:
                self.lineEdit.setText(timeformat)
            else:
                print(timeformat, end='\r')
            time.sleep(1)
            t -= 1
        print('Goodbye!\n\n\n\n\n')

    def strToSec(self, s):
        mins = s[:2]
        secs = s[3:]
        return int(mins) * 60 + int(secs)
    def test(self):
        print("testing...")

if __name__ == "__main__":
    t = Timer()
    t.countdown(t.strToSec("02:00"))