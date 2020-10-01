from datetime import datetime, date
from bme280 import BME280       #Enviro+'s Temperature sensor library.
from pms5003 import PMS5003, ReadTimeoutError #Enviro+'s Particulates sensor library.
import logging

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus

global currentDay, writeLog, bme280, pms5003

def logWeather():
    temperature = bme280.get_temperature()
    pressure = bme280.get_pressure()
    humidity = bme280.get_humidity()
    particulateReading = pms5003.read()
    except ReadTimeoutError:
        pms5003 = PMS5003()

    print('[' + str(datetime.now()) + ']: Temperature (*C): ' + str(temperature) + '\tPressure (hPa): ' + str(pressure) + '\tHumidity (%): ' + str(humidity) + '\tParticulates : ' + str(particulateReading) + '\n')
    logging.info(str(temperature) + '\t\t\t\t' str(pressure) + '\t\t\t' +  str(humidity) + '\t\t' + str(particulateReading))

def generateLogFile():
    logging.basicConfig(format='%(asctime)s: %(message)s', filename='AutoWeatherLog' + str(date.today()) + '.log', level=logging.INFO)
    logging.info('Started logging from script.')

def userSurvey():
    global userWantsAutomaticTemperatureTracking, tempCheckFrequency
    userWantsAutomaticTemperatureTracking = input("Do you want continuous temperature tracking? (Y/N): ")
    if userWantsAutomatic.lower() == 'y' or userWantsAutomatic.lower() == 'yes':
        userWantsAutomaticTemperatureTracking = True
        try:
            tempCheckFrequency = float(input("How often do you want to check temperatures? (in minutes): "))
        except:
            tempCheckFrequency = float(input("Please give a valid number input in minutes: "))
            logging.info('Script taking info every ' + str(tempCheckFrequency) + ' minutes.')
    else:
        userWantsAutomaticTemperatureTracking = False
        logging.info('userWantsAutomaticTemperatureTracking: ' + str(userWantsAutomaticTemperatureTracking))
    logging.info('Temperature (*C): \t\t Pressure (hPa): \t\t Humidity (%): \t\t Particulates: ')


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