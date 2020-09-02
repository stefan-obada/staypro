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
from kivy.lang.builder import Builder
from kivy.core.window import Window
from kivy.clock import Clock

from kivy.properties import ObjectProperty, StringProperty


class BaseLayout(ABC):
    """ Protocol for all layouts in the app. """

    @abstractmethod
    def exit_point(self, screen):
        """ Should unbind everything from keyboard and do """
        return NotImplementedError

    @abstractmethod
    def _entry_point(self):
        """ Should change the screen and bind keyboard inputs """


class MainLayout(Screen):

    def entry_point(self):
        Window.bind(on_key_down=self.keyact)

    def exit_point(self, screen):
        pass

    def keyact(self, *args):
        key_code = args[1]
        if key_code == 13:  # Enter key
            print("Starting activity...")
            self.start_activity()

    def start_activity(self):
        # Set RUNTIME text to activity and start timer
        runtime_screen = self.manager.get_screen("runtime")
        runtime_screen.start_timer()
        runtime_screen.update_activity(activity=self.ids.main_activity.text)

        # Set screen
        self.manager.current = "runtime"


class LoginLayout(Screen):

    def entry_point(self):
        Window.bind(on_key_down=self.keyact)

    def exit_point(self, screen):
        Window.unbind(on_key_down=self.keyact)
        self.manager.get_screen(screen).entry_point()
        self.manager.current = screen

    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)
        self.entry_point()

    def keyact(self, *args):
        key_code = args[1]
        if key_code == 13:  # Enter key
            print("Checking login...")
            self.check_login()

    def check_login(self):
        user = self.ids.login_user.text
        pwd = self.ids.login_pwd.text
        if user is "a" and pwd is "b":
            # TODO change this to Database
            self.exit_point("main")
        else:
            print(self)
            self.add_widget(Label(text="Invalid", color=(1, 0, 0, 1)))



class RuntimeLayout(Screen):

    def entry_point(self):
        pass

    def exit_point(self, screen):
        pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.bind()
        self.paused = False

    def keydown(self, *args):
        print("null")

    def stop(self):
        self.stop_timer()
        self.manager.current = "main"

    def update_time(self, start_time, *args):
        eta = datetime.timedelta(seconds=(int(time.time() - start_time)))
        processed_eta = eta.__str__()
        self.ids.runtime_current_time.text = processed_eta

    def update_activity(self, activity):
        self.ids.runtime_current_activity.text = activity

    def start_timer(self):
        start_time = time.time()
        self.timer = Clock.schedule_interval(partial(self.update_time, start_time), 1)

    def stop_timer(self):
        if self.timer:
            self.timer.cancel()

    def pause_timer(self):
        if self.paused:
            self.start_timer()
            self.ids.runtime_pause_btn.text = "PAUSE"
            self.paused = False
        else:
            start_pause_time = time.time()
            self.stop_timer()
            self.ids.runtime_pause_btn.text = "RESUME"
            self.paused = True


class MainApp(App):

    def __init__(self, *args, **kwargs):
        super(MainApp, self).__init__(*args, **kwargs)
        self.sm = ScreenManager()

    def build(self):
        Builder.load_file("main.kv")
        self.sm.add_widget(LoginLayout(name="login"))
        self.sm.add_widget(MainLayout(name="main"))
        self.sm.add_widget(RuntimeLayout(name="runtime"))
        return self.sm


if __name__ == '__main__':
    MainApp().run()

# # Get screen size
# w_screen, h_screen = sg.Window.get_screen_size()
# sg.theme('TanBlue')
# # #

# # Log file
# if not path.isdir('SP_log'):
#     mkdir('SP_log')
# log_path = 'SP_log/' + 'log.csv'
#
# if not path.isfile(log_path):  # First usage per day
#     with open(log_path, 'w') as first_file:
#         first_file.write('Date,Activity,Minutes,Seconds\n')
#         # Next row is for future implementation
#         # first_file.write('Activity,Start,End,Minutes,Seconds\n')
#
# # #
#
# # Build 1st window
# layout1 = [
#     [sg.InputText(default_text='', key='-ACTIVITY-', focus=True, size=(26, 1))],
#     [sg.Button(button_text='GO', key='go', bind_return_key=True), sg.Button(button_text='EXIT', key='exit')]
# ]
# window1 = sg.Window(title='StayPro', layout=layout1, location=(0, h_screen - 150), use_ttk_buttons=True,
#                     alpha_channel=0.85, grab_anywhere=True, element_justification='center', keep_on_top=True)
#
#
# # #
#
#
# def current_time(start_time, lost_time):
#     """ Time accounting for pauses """
#     return int(round(time.time() * 100)) - start_time - int(round(lost_time * 100))
#
#
# def update_log(activity, start_time, lost_time):
#     # Next 2 rows are for future implementation
#     # end_ascii_time = time.asctime().split()[3]
#     # start_ascii_time = time.ctime(start_time).split()[3]
#
#     try:
#         with open(log_path, 'a') as log_file:
#             ct = current_time(start_time, lost_time)
#             log_file.write("{},{},{:02d},{:02d}\n".format(date.today().isoformat(),
#                                                           activity, (ct // 100) // 60, (ct // 100) % 60))
#     except PermissionError as e:
#         sg.Popup('Please close the LOG file.', title='ERROR', )
#         update_log(activity, start_time, lost_time)
#
#
# def main():
#     while True:
#         event, values = window1.read()
#
#         if event in (None, 'exit'):  # Sys close or Exit
#             window1.close()
#             break
#
#         elif event == 'go':  # Press GO, change to window2
#
#             # Get the previous input and hide window1
#             activity = values['-ACTIVITY-']
#             window1.hide()
#             # #
#
#             # Build 2nd window
#             layout2 = [
#                 [sg.Text(activity, key='-CURRENT_ACTIVITY-'), sg.Text('Time:', key='-TIME-')],
#                 [sg.Button(button_text='PAUSE', key='pause', auto_size_button=True),
#                  sg.Button(button_text='CANCEL', key='cancel')]
#             ]
#             window2 = sg.Window(title='StayPro', layout=layout2, location=(0, h_screen - 150), use_ttk_buttons=True,
#                                 alpha_channel=0.85, grab_anywhere=True, element_justification='center',
#                                 keep_on_top=True,
#                                 return_keyboard_events=True)
#             # #
#
#             start_time = int(round(time.time() * 100))
#             lost_time = 0  # used for counting time in pauses
#             window2_finished = False
#
#             while not window2_finished:  # Window 2 loop
#                 event, values = window2.read(timeout=10)
#
#                 if event in (None, 'cancel'):  # If cancel, return to window1, update log
#                     update_log(activity, start_time, lost_time)
#
#                     # window2_finished = True # Useless
#                     window2.close()
#                     window1.un_hide()
#                     break
#
#                 elif event == 'pause':  # PAUSE loop (if PAUSE/Space are pressed)
#                     start_pause_time = time.time()
#
#                     window2['pause'].update('RESUME')
#
#                     while True:  # PAUSE Loop until RESUME/Space is pressed
#                         event, values = window2.read()
#
#                         if event in (None, 'cancel'):  # Go back to window1, update log
#
#                             # Update log in 'a' mode
#                             update_log(activity, start_time, lost_time)
#
#                             window2_finished = True
#                             window2.close()
#                             window1.un_hide()
#                             break
#
#                         elif event == 'pause':  # If RESUME or Space is pressed, stay chill
#                             lost_time = lost_time + time.time() - start_pause_time
#                             window2['pause'].update('PAUSE')
#                             break
#
#                 ct = current_time(start_time, lost_time)
#                 window2['-TIME-'].update('{:02d}:{:02d}'.format((ct // 100) // 60,
#                                                                 (ct // 100) % 60))
#
#         else:  # Any other button is pressed, do nothing
#             pass
#
