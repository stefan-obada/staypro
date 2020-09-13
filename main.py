from abc import abstractmethod, ABC

import os
import time
import datetime
from functools import partial

import kivy
from kivy.config import Config
from utils.config import generate_config_path
from kivy.utils import platform

# This has to be done before importing all other uix modules
kivy.require("1.11.1")
Config.read(generate_config_path(platform=platform))
# #

from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.label import Label
from kivy.uix.screenmanager import FallOutTransition, FadeTransition, WipeTransition
from kivy.lang.builder import Builder
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.logger import Logger

from timer import get_timer

UPDATE_INTERVAL = 0.1


class BaseLayout(ABC):
    """ Protocol for all layouts in the app. """

    def exit(self, screen, *args, **kwargs):
        Window.unbind(on_key_down=self.keyact)
        self.manager.get_screen(screen).entry(*args, **kwargs)
        self.manager.current = screen

        self.exit_add(*args)

    def entry(self, *args, **kwargs):
        Window.bind(on_key_down=self.keyact)

        self.entry_add(*args, **kwargs)

    @abstractmethod
    def keyact(self, *args):
        """ This should capture every key """
        return NotImplementedError

    def entry_add(self, *args, **kwargs):
        """ What else do you want when entering """
        pass

    def exit_add(self, *args, **kwargs):
        """ What else do you want when exiting """
        pass


class MetaMerge(type(Screen), type(BaseLayout)):
    pass


class LoginLayout(BaseLayout, Screen, metaclass=MetaMerge):

    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)
        self.entry_add()

    def keyact(self, *args):
        key_code = args[1]
        if key_code == 13:  # Enter key
            print("Checking login...")
            self.check_login()

    def check_login(self):
        user = self.ids.login_user.text
        pwd = self.ids.login_pwd.text
        Logger.info(f"LOGIN: User {user} attempting login.")
        if user is "a" and pwd is "b":
            # TODO change this to Database
            self.exit(screen="main")
        else:
            print(self)
            self.add_widget(Label(text="Invalid", color=(1, 0, 0, 1)))


class MainLayout(BaseLayout, Screen, metaclass=MetaMerge):

    def keyact(self, *args):
        key_code = args[1]
        if key_code == 13:  # Enter key
            print("Starting activity...")
            self.start_activity()

    def start_activity(self):
        self.exit(screen="runtime", activity=self.ids.main_activity.text)


class RuntimeLayout(BaseLayout, Screen, metaclass=MetaMerge):

    def keyact(self, *args):
        pass

    def entry_add(self, *args, **kwargs):
        # Set activity
        self.activity = kwargs.get("activity", "None")
        self.ids.runtime_current_activity.text = self.activity

        # Start timer
        self.timer = get_timer(activity=self.activity, update_interval=UPDATE_INTERVAL/3)
        self.timer.start()
        self.paused = False

        # Make sure button is on PAUSED
        self.ids.runtime_pause_btn.text = "PAUSE"

        # Schedule time update on screen
        Clock.schedule_interval(self.update_time, self.timer.update_interval/2)

    def exit_add(self, *args, **kwargs):
        self.timer.stop()
        orm.upload_activity(timer=self.timer)


    def stop(self):
        self.exit(screen="main")

    def pause(self):
        if not self.paused:
            # Pause timer
            self.timer.pause()
            self.paused = True

            # Switch button from "PAUSE" to "RESUME"
            self.ids.runtime_pause_btn.text = "RESUME"

            return

        if self.paused:
            # Re-start the time
            self.timer.start()
            self.paused = False

            # Switch button from "RESUME" to "PAUSE"
            self.ids.runtime_pause_btn.text = "PAUSE"

            return

    def update_time(self, *args):
        self.ids.runtime_current_time.text = self.timer.get_hhmmss()


class MainApp(App):

    def __init__(self, *args, **kwargs):
        super(MainApp, self).__init__(*args, **kwargs)
        self.sm = ScreenManager(transition=FallOutTransition())

    def build(self):
        Builder.load_file("main.kv")
        self.sm.add_widget(LoginLayout(name="login"))
        self.sm.add_widget(MainLayout(name="main"))
        self.sm.add_widget(RuntimeLayout(name="runtime"))
        return self.sm


if __name__ == '__main__':
    MainApp().run()