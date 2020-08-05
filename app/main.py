# import PySimpleGUI as sg
# import time
# from datetime import date
# from os import path, mkdir
import os


import kivy
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.lang.builder import Builder
from kivy.utils import platform
from kivy.config import Config
from utils.config import generate_config_path
Config.read(generate_config_path(platform=platform))
from kivy.core.window import Window



# Load config and require kivy version
kivy.require("1.11.1")



class MainLayout(Screen):
    pass


class LoginLayout(Screen):
    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)
        Window.bind(on_key_down=self.keyact)

    def keyact(self, *args):
        key_code = args[1]
        if key_code == 13: # Enter key
            # TODO this results in a bug right now
            self.check_login()

    def check_login(self, user, pwd):
        if user is "a" and pwd is "b":
            # TODO change this to Database
            self.manager.current = "main"
        else:
            print(self)
            self.add_widget(Label(text="Invalid", color = (1,0,0,1)))


class RuntimeLayout(Screen):

    def keyact(self, *args):
        pass


class MainApp(App):
    def build(self):
        return Builder.load_file("main.kv")


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
