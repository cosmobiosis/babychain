import time

class Timer():
    def __init__(self):
        self.block_countdown_time = 15
        self.time_format = "None"
        self.clear_to_send = True
        return

    def countdown(self):
        timeleft = self.block_countdown_time
        while timeleft > 0:
            mins, secs = divmod(timeleft, 60)
            self.time_format = '{:02d}:{:02d}'.format(mins, secs)
            time.sleep(1)
            timeleft -= 1
        self.clear_to_send = True
        return "Countdown Ends! Ready for a new block!"
