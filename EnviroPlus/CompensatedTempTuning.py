#!/usr/bin/env python3

import time
from bme280 import BME280
from datetime import datetime, date
import logging
import requests
import json



try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus


logging.basicConfig(
    format='%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

logging.info("""compensatedTempTuner.py - Using CPU Temp, Open Weather Map API, and BME sensors, tune the compensation factor to get a calibrated reading. 
Method adapted from Initial State's Enviro pHAT review:
https://medium.com/@InitialState/tutorial-review-enviro-phat-for-raspberry-pi-4cd6d8c63441

Press Ctrl+C to exit!

""")

bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)


# Get the temperature of the CPU for compensation
def get_cpu_temperature():
    with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
        temp = f.read()
        temp = int(temp) / 1000.0
    return temp

def get_open_weather_temp():
    URL = 'https://api.openweathermap.org/data/2.5/onecall?lat=' +str(lat) + '&lon=' + str(lon) +  '&appid=' + APIKey + '&units=metric'
    response = requests.get(URL)
    if not response.ok:
        print ('HTTP Response: ' , response.status_code , response.reason)
    responseObj = response.json()
    
    return responseObj["current"]["temp"]

def get_Factor(OpenWeather_temp, CPU_temp, BME_temp):
    return abs((CPU_temp - BME_temp)/(OpenWeather_temp - BME_temp))


APIKey = '7474a222b6f393d616e11301d843b04d'
lat = '40.765031'
lon = '-111.849385'
discardedFirstReading = False

cpu_temps = [get_cpu_temperature()] * 5

calculatedFactors = []

while True:
    cpu_temp = get_cpu_temperature()
    # Smooth out with some averaging to decrease jitter
    cpu_temps = cpu_temps[1:] + [cpu_temp]
    avg_cpu_temp = sum(cpu_temps) / float(len(cpu_temps))
    raw_temp = bme280.get_temperature()
    open_weather_map_temp = float(get_open_weather_temp())
    factor = get_Factor(open_weather_map_temp, avg_cpu_temp, raw_temp)
    comp_temp = raw_temp - ((avg_cpu_temp - raw_temp) / factor)
    
    if discardedFirstReading:
        calculatedFactors.append(factor)
        logging.info(("Average Factor: {:05.2f}".format(sum(calculatedFactors)/len(calculatedFactors))))
    else:
        discardedFirstReading = True
    
    logging.info(("Compensated temperature: {:05.2f} *C".format(comp_temp)) + ("\tOpen Weather temperature: {:05.2f} *C".format(open_weather_map_temp))+("\tBME temperature: {:05.2f} *C".format(raw_temp))+("\t Factor: \t{:05.2f}".format(factor)))
    
    time.sleep(2)

