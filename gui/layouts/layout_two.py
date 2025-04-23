import FreeSimpleGUI as sg

def layout_window2():
    layout_two = [[sg.Push(background_color='light grey'),
                   sg.Text('Sit completely still and focus on the red dot.',
                           text_color='black',
                           font=('Times New Roman', 20),
                           auto_size_text=True,
                           background_color='light grey')],
                  [sg.Push(background_color='light grey'),
                   sg.Text('Blink once each time the color changes.',
                           text_color='black',
                           font=('Times New Roman', 20),
                           auto_size_text=True,
                           background_color='light grey'),
                   sg.Push(background_color='light grey')],
                  [sg.Text(background_color='light grey')],
                  [sg.Text(background_color='light grey')],
                  [sg.Push(background_color='light grey'),
                   sg.Text('🔴',
                           key='-DOT-',
                           font=('Arial,', 40),
                           background_color='light grey'),
                   sg.Push(background_color='light grey')]
                  ]
    return layout_two