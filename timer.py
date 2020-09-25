import threading
from kivy.logger import Logger
from multiprocessing import Process
import time


def get_timer(activity, update_interval=0.5):
    timer = Timer(activity=activity, update_interval=update_interval)
    timer.load()
    return timer


class Timer:
    """
    Timer instance shall be used to track only a single activity.
    Load thread with load()
    Destroy thread with stop()
    """

    def __init__(self, activity="", update_interval=0.5):
        self.update_interval = update_interval
        self.activity = activity
        self.__time = 0

    def log_info(self, message: str):
        Logger.info(f"{self.activity}: {message}")

    def load(self):
        self.thread = threading.Thread(target=self.update_time)
        self.log_info("Timer loaded.")

    def update_time(self):
        while True:
            if self.paused:
                return

            self.__time += self.update_interval
            time.sleep(self.update_interval)

    def start(self):
        if hasattr(self, "thread") and not self.thread.is_alive():
            self.load()
        elif not hasattr(self, "thread"):
            self.load()

        self.paused = False
        self.thread.start()
        self.log_info("Timer started.")


    def stop(self):
        self.paused = True
        self.thread.join()
        self.log_info("Timer stopped.")

    def pause(self):
        self.paused = True
        self.thread.join()
        self.log_info("Timer paused.")

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
        secs = int(self.__time)

        mins, secs = divmod(secs, 60)
        hours, mins = divmod(mins, 60)

        if secs < 10:
            str_secs = f"0{secs}"
        else:
            str_secs = f"{secs}"

        if mins < 10:
            str_mins = f"0{mins}"
        else:
            str_mins = f"{mins}"

        if hours < 10:
            str_hours = f"0{hours}"
        else:
            str_hours = f"{hours}"

        if hours == 0:
            return f"{str_mins}:{str_secs}"
        else:
            return f"{str_hours}:{str_mins}:{str_secs}"


