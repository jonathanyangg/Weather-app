import PySimpleGUI as sg 
from bs4 import BeautifulSoup as bs
import requests

def get_weather_data(location):
    url = f'https://www.google.com/search?q=weather+{location.replace(" ","")}'
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    html = session.get(url)

    soup = bs(html.text, "html.parser")
    name = soup.find("div", attrs={'id': 'wob_loc'}).text
    time = soup.find("div", attrs={'id': 'wob_dts'}).text
    weather = soup.find("span", attrs={'id': 'wob_dc'}).text
    temp = soup.find("span", attrs={'id': 'wob_tm'}).text
    return name, time, weather, temp


sg.theme("black")
image_col = sg.Column([
    [sg.Image(key = "-IMAGE-", background_color = "#FFFFFF")]
    ])
info_col = sg.Column([
    [sg.Text('', key = '-LOCATION-', font = 'Arial 24', background_color = '#000000', text_color = '#FFFFFF', pad = 0, visible = False)],
    [sg.Text('', key = '-TIME-', font = 'Arial 20', background_color = '#000000', text_color = '#FFFFFF', pad = 0, visible = False)],
    [sg.Text('', key = '-TEMP-', font = 'Arial 20', pad = 0, background_color = '#000000', text_color = '#FFFFFF', visible = False)],
    [sg.Text('', key = '-WEATHER-', font = 'Arial 20', pad = 0, background_color = '#000000', text_color = '#FFFFFF', visible = False)]
    ],key = '-RIGHT-',
    background_color = '#000000')

layout = [
    [sg.Input(expand_x = True, key = "-INPUT-"), sg.Button("Search", button_color = "#555555")],
    [sg.Text("Weather App")],
    [image_col, info_col],
]

window = sg.Window('Weather', layout)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break

    if event == "Search":
        name, time, weather, temp = get_weather_data(values["-INPUT-"])
        window["-LOCATION-"].update(name, visible = True)
        window["-TIME-"].update(time, visible = True)
        window["-TEMP-"].update(temp, visible = True)
        window["-WEATHER-"].update(weather, visible = True)

        if int(temp) > 20:
            window["-IMAGE-"].update("/Users/jonathanyang/Desktop/weather/hot.png")
        elif int(temp) > 0:
            window["-IMAGE-"].update("/Users/jonathanyang/Desktop/weather/medium.png")
        else:
            window["-IMAGE-"].update("/Users/jonathanyang/Desktop/weather/cold.png")
window.close()
