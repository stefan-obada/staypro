import PySimpleGUI as sg
import time

w_screen, h_screen = sg.Window.get_screen_size()
sg.theme('TanBlue')

# Build 1st window
layout1 = [
    [sg.InputText(default_text='', key='-ACTIVITY-', focus=True, size=(26, 1))],
    [sg.Button(button_text='GO', key='go', bind_return_key=True), sg.Button(button_text='EXIT', key='exit')]
]

window1 = sg.Window(title='StayPro', layout=layout1, location=(0, h_screen-150), use_ttk_buttons=True,
                    alpha_channel=0.85, grab_anywhere=True, element_justification='center', keep_on_top=True)


def main():
    while True:
        event, values = window1.read()

        if event in (None, 'exit'):  # Sys close or Exit
            window1.close()
            break

        elif event == 'go':  # Press GO, change to window2

            # Get the previous input and hide window1
            activity = values['-ACTIVITY-']
            window1.hide()

            # Build 2nd window
            layout2 = [
                [sg.Text(activity, key='-CURRENT_ACTIVITY-'), sg.Text('Time:', key='-TIME-')],
                [sg.Button(button_text='PAUSE', key='pause', auto_size_button=True), sg.Button(button_text='CANCEL', key='cancel')]
            ]
            window2 = sg.Window(title='StayPro', layout=layout2, location=(0, h_screen-150), use_ttk_buttons=True,
                                alpha_channel=0.85, grab_anywhere=True, element_justification='center', keep_on_top=True,
                                return_keyboard_events=True)

            start_time = int(round(time.time() * 100))
            lost_time = 0

            while True: # Window 2 loop
                event, values = window2.read(timeout=10)

                if event in (None, 'cancel'): # If cancel, return to window1
                    window2.close()
                    window1.un_hide()
                    break

                elif event == 'pause':
                    start_pause_time = time.time()
                    window2['pause'].update('RESUME')
                    while True:
                        event, values = window2.read()

                        if event in (None, 'cancel'):
                            window2.close()
                            window1.un_hide()
                            break

                        elif event == 'pause':
                            lost_time = lost_time + time.time() - start_pause_time
                            window2['pause'].update('PAUSE')
                            break

                current_time = int(round(time.time() * 100)) - start_time - int(round(lost_time*100))
                window2['-TIME-'].update('{:02d}:{:02d}'.format((current_time // 100) // 60,
                                                                  (current_time // 100) % 60))


        else:  # Any other button is pressed
            pass


if __name__ == '__main__':
    main()
