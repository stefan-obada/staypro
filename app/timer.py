import threading
from kivy.logger import Logger
from multiprocessing import Process
import time

def get_timer():
    timer = Timer()
    timer.load()
    return timer


class Timer:
    """
    Timer instance shall be used to track only a single activity.
    Load with load()
    Destroy with stop()
    """
    def __init__(self, activity="", update_interval=0.5):
        self.update_interval = update_interval
        self.activity = activity
        self.__time = 0
        self.paused = False

    def log_info(self, message: str):
        Logger.info(f"{self.activity}: {message}")

    def load(self):
        self.thread = threading.Timer(interval=self.update_interval, function=self.update_time)
        self.log_info("Timer loaded.")

    def update_time(self):
        self.__time += self.update_interval

    def start(self):
        self.thread.start()
        self.log_info("Timer started.")
        self.paused = False

    def stop(self):
        self.thread.cancel()
        self.log_info("Timer stopped.")

    def pause(self):
        self.stop()
        self.log_info("Timer paused.")
        self.paused = True

    @property
    def time(self):
        return self.__time

    @time.setter
    def time(self, new_time):
        if new_time > 0:
            self.__time = new_time
        else:
            self.__time = 0

    def get_hhmmss(self):
        secs = self.__time
        mins, secs = divmod(secs, 60)
        hours, mins = divmod(mins, 60)

        if mins == 0:
            return f"{secs}"
        elif hours == 0:
            return f"{mins}:{secs}"
        else:
            return f"{hours}:{mins}:{secs}"
