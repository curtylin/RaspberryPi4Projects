from datetime import datetime, date
from bme280 import BME280       #Enviro+'s Temperature sensor library.
from pms5003 import PMS5003, ReadTimeoutError #Enviro+'s Particulates sensor library.
import logging
import time
from CompensatedTemp import get_compensated_temperature

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus

global currentDay, writeLog, bme280, pms5003

def logWeather():
    global pms5003
    temperature = get_compensated_temperature(1.5)
    pressure = bme280.get_pressure()
    humidity = bme280.get_humidity()
    try:
        particulateReading = pms5003.read()
    except ReadTimeoutError:
        pms5003 = PMS5003()

    print('[' + str(datetime.now()) + ']: Temperature (*C): ' + str(temperature) + '\tPressure (hPa): ' + str(pressure) + '\tHumidity (%): ' + str(humidity) + '\nParticulates : ' + str(particulateReading) + '\n')
    logging.info('[' + str(datetime.now()) + ']: Temperature (*C): ' + str(temperature) + '\tPressure (hPa): ' + str(pressure) + '\tHumidity (%): ' + str(humidity) + '\nParticulates : ' + str(particulateReading) + '\n')

def generateLogFile():
    logging.basicConfig(format='%(asctime)s: %(message)s', filename='AutoWeatherLog' + str(date.today()) + '.log', level=logging.INFO)
    logging.info('Started logging from script.')

def userSurvey():
    global userWantsAutomaticTemperatureTracking, tempCheckFrequency
    userWantsAutomaticTemperatureTracking = input("Do you want continuous temperature tracking? (Y/N): ")
    if userWantsAutomaticTemperatureTracking.lower() == 'y' or userWantsAutomaticTemperatureTracking.lower() == 'yes':
        userWantsAutomaticTemperatureTracking = True
        try:
            tempCheckFrequency = float(input("How often do you want to check temperatures? (in minutes): "))
        except:
            tempCheckFrequency = float(input("Please give a valid number input in minutes: "))
            logging.info('Script taking info every ' + str(tempCheckFrequency) + ' minutes.')
    else:
        userWantsAutomaticTemperatureTracking = False
        logging.info('userWantsAutomaticTemperatureTracking: ' + str(userWantsAutomaticTemperatureTracking))


# Inital setup for the script includes automatic temp tracking, setup of sensors, logging, etc.
userWantsAutomaticTemperatureTracking = True
tempCheckFrequency = 5
currentDay = str(date.today())
bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)
pms5003 = PMS5003()

generateLogFile()
userSurvey()

if userWantsAutomaticTemperatureTracking:
    while userWantsAutomaticTemperatureTracking:
        if currentDay != str(date.today()):     #Script automatically generates a new log file at the start of a new day.
            logging.FileHandler.close()
            generateLogFile()
        logWeather()
        time.sleep(tempCheckFrequency*60)
else:
    logWeather()

# writeLog.close()
logging.FileHandler.close()
logging.shutdown()
