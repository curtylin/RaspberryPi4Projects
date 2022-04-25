from pms5003 import PMS5003, ReadTimeoutError #Enviro+'s Particulates sensor library.
import ST7735
from PIL import Image, ImageDraw, ImageFont
from fonts.ttf import RobotoMedium as UserFont
import logging
from datetime import datetime, date
import time
import requests
import json


try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus

global APIKey

def readAPIKey():
    f = open("apiKey.txt", "r")
    APIKey = f.read()
    f.close()
    return APIKey

def displayTwoLines(lineOne, lineTwo, bgColour=(0, 0, 0), textColour=(255, 255, 255)):
    global draw, img, font, pms5003, HEIGHT, WIDTH
    lineOnefont = ImageFont.truetype(UserFont, 15)
    lineTwoFont = ImageFont.truetype(UserFont, 15)

    size_x, size_y = draw.textsize(lineOne, lineOnefont)
    # Calculate text position
    x = (WIDTH - size_x) / 2
    y = ((HEIGHT / 2) - (size_y / 2) ) - 20
    # Draw background rectangle and write text.
    draw.rectangle((0, 0, 160, 80), bgColour)

    draw.text((x, y), lineOne, font=lineOnefont, fill=textColour)

    size_x, size_y = draw.textsize(lineTwo, lineTwoFont)
    # Calculate text position
    x = (WIDTH - size_x) / 2
    y = ((HEIGHT / 2) - (size_y / 2)) + 20
    draw.text((x, y), lineTwo, font=lineTwoFont, fill=textColour)
    disp.display(img.rotate(180))

def displayThreeLines(lineOne, lineTwo, lineThree, bgColour=(0, 0, 0), textColour=(255, 255, 255)):
    global draw, img, font, pms5003, HEIGHT, WIDTH
    lineOnefont = ImageFont.truetype(UserFont, 15)
    lineTwoFont = ImageFont.truetype(UserFont, 15)
    lineThreeFont = ImageFont.truetype(UserFont, 15)

    size_x, size_y = draw.textsize(lineOne, lineOnefont)
    # Calculate text position
    x = (WIDTH - size_x) / 2
    y = ((HEIGHT / 2) - (size_y / 2) ) - 30
    # Draw background rectangle and write text.
    draw.rectangle((0, 0, 160, 80), bgColour)

    draw.text((x, y), lineOne, font=lineOnefont, fill=textColour)

    size_x, size_y = draw.textsize(lineTwo, lineTwoFont)
    # Calculate text position
    x = (WIDTH - size_x) / 2
    y = ((HEIGHT / 2) - (size_y / 2)) - 10
    draw.text((x, y), lineTwo, font=lineTwoFont, fill=textColour)

    size_x, size_y = draw.textsize(lineThree, lineThreeFont)
    # Calculate text position
    x = (WIDTH - size_x) / 2
    y = ((HEIGHT / 2) - (size_y / 2)) + 20
    draw.text((x, y), lineThree, font=lineThreeFont, fill=textColour)

    disp.display(img.rotate(180))



def displayParticulates():
    
    PMmessage = "PM2.5 ug/m3: {}".format(pms5003.read().pm_ug_per_m3(2.5))
    TimeMessage = "Last Update: {}".format(datetime.now().strftime("%H:%M"))
    displayTwoLines(PMmessage, TimeMessage)
    time.sleep(20)



def getTemp():
    lat = '40.765031'
    lon = '-111.849385'
    URL = 'https://api.openweathermap.org/data/2.5/onecall?lat=' +str(lat) + '&lon=' + str(lon) +  '&appid=' + APIKey + '&units=metric'
    response = requests.get(URL)
    if not response.ok:
        print ('HTTP Response: ' , response.status_code , response.reason)
    responseObj = response.json()
    temperature = responseObj["current"]["temp"]
    weather = responseObj["current"]["weather"][0]["main"]

    alerts = []
    try:
        alerts = responseObj["alerts"]
    except:
        pass
    return temperature, weather, alerts


def displayWeather():
    global draw, img, font, HEIGHT, WIDTH, back_colour, text_colour
    tempInfo = getTemp()

    alerts = tempInfo[2]
    if alerts != []:
        for alert in alerts:
            displayTwoLines("Weather Alert:", alert["event"], (255, 0, 0), (0, 0, 0))
            time.sleep(10)
    TimeMessage = "Last Update: {}".format(datetime.now().strftime("%H:%M"))

    TempMessage = "Outside Temp: {}".format(tempInfo[0])
    WeatherMessage = "Weather: {}".format(tempInfo[1])
    displayThreeLines(WeatherMessage, TempMessage, TimeMessage)
    time.sleep(30)




logging.basicConfig(
    format='%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

logging.info("""DisplayParticulates.py" LCD.
Press Ctrl+C to exit!

""")

# Create LCD class instance.
disp = ST7735.ST7735(
    port=0,
    cs=1,
    dc=9,
    backlight=12,
    rotation=270,
    spi_speed_hz=10000000
)

APIKey = readAPIKey()

disp.begin()

# Width and height to calculate text position.
WIDTH = disp.width
HEIGHT = disp.height

# New canvas to draw on.
img = Image.new('RGB', (WIDTH, HEIGHT), color=(0, 0, 0))
draw = ImageDraw.Draw(img)

# Text settings.
font_size = 20
PMfont = ImageFont.truetype(UserFont, font_size)
bus = SMBus(1)
pms5003 = PMS5003()

try:
    while True:
        displayParticulates()
        displayWeather()
    # Turn off backlight on control-c
except KeyboardInterrupt:
    disp.set_backlight(0)