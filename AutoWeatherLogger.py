from datetime import datetime, date
from bme280 import BME280
import logging

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus

global currentDay, userWantsAutomaticTemperatureTracking, tempCheckRecurrance, writeLog

bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)



def logWeather():
    temperature = bme280.get_temperature()
    pressure = bme280.get_pressure()
    humidity = bme280.get_humidity()

    print('[' + str(datetime.now()) + '] \t\t Temperature (*C): ' + str(temperature) + '\t\t Pressure (hPa): ' + str(pressure) + '\t\t Humidity (%): ' + str(humidity) + '\n')
    # writeLog.write('[' + str(datetime.now()) + '] \t\t' + str(temperature) + '\t\t' + str(pressure) + '\t\t' + str(humidity) + '\n')
    logging.info(str(temperature) + '\t\t' str(pressure) + '\t\t' +  str(humidity))

def generateLogFile():
    # writeLogFileName = 'AutoWeatherLog' + str(date.today()) + '.log'
    # writeLog = open(writeLogFileName, 'w', encoding='cp1252')
    # writeLog.write('[' + str(datetime.now()) + '] Started logging from script. \n')
    # writeLog.write('[ Current Time ] \t\t Temperature (*C): \t\t Pressure (hPa): \t\t Humidity (%): \n')
    logging.basicConfig(format='%(asctime)s: %(message)s', filename='AutoWeatherLog' + str(date.today()) + '.log')
    logging.info('Started logging from script.')
    logging.info('Temperature (*C): \t\t Pressure (hPa): \t\t Humidity (%): ')

def userSurvey():
    userWantsAutomaticTemperatureTracking = input("Do you want continuous temperature tracking? (Y/N): ")
    if userWantsAutomatic.lower == 'y' or userWantsAutomatic.lower == 'yes':
        userWantsAutomaticTemperatureTracking = True
        try:
            tempCheckRecurrance = float(input("How often do you want to check temperatures? (in seconds): "))
        except:
            tempCheckRecurrance = float(input("Please give a valid number input in seconds: "))
        # writeLog.write('[' + str(datetime.now()) + '] Script taking info every ' + str(tempCheckRecurrance) + ' seconds. \n')
        logging.info('Script taking info every ' + str(tempCheckRecurrance) + ' seconds.')
    else:
        userWantsAutomaticTemperatureTracking = False
    # writeLog.write('[' + str(datetime.now()) + '] userWantsAutomaticTemperatureTracking: ' + str(userWantsAutomaticTemperatureTracking) + '\n')
    logging.info('userWantsAutomaticTemperatureTracking: ' + str(userWantsAutomaticTemperatureTracking))



userWantsAutomaticTemperatureTracking = True
tempCheckRecurrance = 60
currentDay = str(date.today())

generateLogFile()
userSurvey()

if userWantsAutomaticTemperatureTracking:
    while userWantsAutomaticTemperatureTracking:
        if currentDay != str(date.today()):     #Script automatically generates a new log file at the start of a new day.
            # writeLog.close()
            logging.FileHandler.close()
            generateLogFile()
        logWeather()
        time.sleep(tempCheckRecurrance)
else:
    logWeather()

# writeLog.close()
logging.FileHandler.close()
logging.shutdown()