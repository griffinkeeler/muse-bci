import FreeSimpleGUI as sg

def layout_window3():
    layout_three = [[sg.Text(background_color='light grey')],
                    [sg.Text(background_color='light grey')],
                    [sg.Text(background_color='light grey')],
                    [sg.Text(background_color='light grey')],
                    [sg.Push(background_color='light grey'),
                     sg.Text("Calibration Complete!",
                             font=('Times New Roman', 20),
                             text_color='black',
                             background_color='light grey'),
                     sg.Push(background_color='light grey')],
                    [[sg.Push(background_color='light grey'),
                      sg.Button('View Results',
                                font=('Helvetica', 16)),
                      sg.Push(background_color='light grey')]],
                    [[sg.Push(background_color='light grey'),
                      sg.Text(key='-VIEW_THRESHOLD-',
                              background_color='light grey'),
                      sg.Push(background_color='light grey')]],
                    [sg.Text(background_color='light grey')],
                    [sg.Text(background_color='light grey')],
                    [sg.Text(background_color='light grey')]
                    ]
    return layout_three