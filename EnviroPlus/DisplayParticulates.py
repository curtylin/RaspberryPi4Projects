from pms5003 import PMS5003, ReadTimeoutError #Enviro+'s Particulates sensor library.
import ST7735
from PIL import Image, ImageDraw, ImageFont
from fonts.ttf import RobotoMedium as UserFont
import logging
from datetime import datetime, date
import time

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus




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

disp.begin()

# Width and height to calculate text position.
WIDTH = disp.width
HEIGHT = disp.height

# New canvas to draw on.
img = Image.new('RGB', (WIDTH, HEIGHT), color=(0, 0, 0))
draw = ImageDraw.Draw(img)

# Text settings.
font_size = 20
font = ImageFont.truetype(UserFont, font_size)
timeFont = ImageFont.truetype(UserFont, 15)
text_colour = (255, 255, 255)
back_colour = (0, 0, 0)


checkFrequency = 1
bus = SMBus(1)
pms5003 = PMS5003()

try:
    while True:
        TimeMessage = "Last Update: {}".format(datetime.now().strftime("%H:%M"))
        PMmessage = "PM2.5 ug/m3: {}".format(pms5003.read().pm_ug_per_m3(2.5))

        size_x, size_y = draw.textsize(TimeMessage, timeFont)
        # Calculate text position
        x = (WIDTH - size_x) / 2
        y = ((HEIGHT / 2) - (size_y / 2) ) - 20

        # Draw background rectangle and write text.
        draw.rectangle((0, 0, 160, 80), back_colour)
        draw.text((x, y), TimeMessage, font=timeFont, fill=text_colour)


        size_x, size_y = draw.textsize(PMmessage, font)
        # Calculate text position
        x = (WIDTH - size_x) / 2
        y = ((HEIGHT / 2) - (size_y / 2)) + 20
        draw.text((x, y), PMmessage, font=font, fill=text_colour)



        disp.display(img.rotate(180))
        time.sleep(checkFrequency * 60)   
    # Turn off backlight on control-c
except KeyboardInterrupt:
    disp.set_backlight(0)