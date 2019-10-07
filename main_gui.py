import PySimpleGUI as sg
from PIL import Image, ImageDraw
import image_grabber
import image_reader
import wf_market_request
from urllib.error import HTTPError

image_path = './images/{}.png'.format


def full_window():
    # All the stuff inside your window.
    layout = [[sg.Text('Capture Relic screen')],
              [sg.Frame(
                  layout=[[sg.Text('X', size=(5, 1)),
                           sg.InputText(size=(10, 1), default_text='480'),
                           sg.Text('Y', size=(5, 1)),
                           sg.InputText(size=(10, 1), default_text='415')],
                          [sg.Text('Width', size=(5, 1)),
                           sg.InputText(size=(10, 1), default_text='970'),
                           sg.Text('Height', size=(5, 1)),
                           sg.InputText(size=(10, 1), default_text='45')],
                          [sg.Text('Mates', size=(5, 1)),
                           sg.InputText(size=(10, 1), default_text='4')]],
                  title='Options')],
              [sg.Button('Capture'), sg.Button('Cancel')]]

    # Create the Window
    window = sg.Window('Window Title', layout)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()

        print(values)

        if event in ('Capture', ''):
            image_container(int(values[0]), int(values[1]), int(values[2]), int(values[3]), int(values[4]))

        if event in (None, 'Cancel'):  # if user closes window or clicks cancel
            break

    window.close()


def popup(data):
    sg.Popup(str(data))


def image_container(x, y, width, height, mates):
    image_grabber.grab_image(x, y, width, height, mates)

    text = []
    for i in range(0, mates):
        ocr_result = image_reader.ocr(image_path('capture_{}'.format(i)))
        text.append(ocr_result['text'])

    formatted_text = ''
    for i, text_frag in enumerate(text):
        if i != len(text) - 1:
            formatted_text += text_frag + ' --- '
        else:
            formatted_text += text_frag

    items = []
    for item in text:
        request_name = item.lower().strip().replace(' ', '_')
        data = 'No data found for "{}"'.format(request_name)

        try:
            data = wf_market_request.request_item_prices(request_name)
        except HTTPError or UnicodeEncodeError:
            print('Site not found!')

        if data is None:
            return

        items.append(data)

    formatted_items = ''
    for i, data_frag in enumerate(items):
        if i != len(text) - 1:
            formatted_items += data_frag + '\n'
        else:
            formatted_items += data_frag

    layout = [
        [sg.Text('Captured Relic Data')],
        [sg.Image(filename=image_path('capture'))],
        [sg.Text(str(formatted_text))],
        [sg.Text(str(formatted_items))],
    ]

    window = sg.Window('Screen Capture', layout)
    while True:
        event, values = window.read()
        if event in (None, ''):  # if user closes window
            break

    window.close()


full_window()
