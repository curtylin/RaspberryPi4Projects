from datetime import datetime, date
import logging
import time
import requests
import json

global currentDay, userWantsAutomaticTemperatureTracking, tempCheckRecurrance
global lat, lon, APIKey

def logWeather():
    response = requests.get('https://api.openweathermap.org/data/2.5/onecall?lat={0}&lon={1}&appid={2}' % str(lat), str(lon), APIKey)
    responseObj = json.loads(response)
    
    temperature = responseObj.current.temp
    pressure = responseObj.current.pressure
    humidity = responseObj.current.humidity

    print('[' + str(datetime.now()) + '] \t\t Temperature (*C): ' + str(temperature) + '\t\t Pressure (hPa): ' + str(pressure) + '\t\t Humidity (%): ' + str(humidity) + '\t\t Particulates : ' + str(particulateReading) + '\n')
    # # writeLog.write('[' + str(datetime.now()) + '] \t\t' + str(temperature) + '\t\t' + str(pressure) + '\t\t' + str(humidity) + '\n')
    logging.info(str(temperature) + '\t\t' + str(pressure) + '\t\t' +  str(humidity))

def generateLogFile():
    # writeLogFileName = 'AutoWeatherLog' + str(date.today()) + '.log'
    # writeLog = open(writeLogFileName, 'w', encoding='cp1252')
    # writeLog.write('[' + str(datetime.now()) + '] Started logging from script. \n')
    # writeLog.write('[ Current Time ] \t\t Temperature (*C): \t\t Pressure (hPa): \t\t Humidity (%): \n')
    logging.basicConfig(format='%(asctime)s: %(message)s', filename='AutoWeatherLog' + str(date.today()) + '.log', level=logging.INFO)
    logging.info('Started logging from script.')
    logging.info('Temperature (*C): \t\t Pressure (hPa): \t\t Humidity (%): \t\t Particulates: ')

def userSurvey():
    userWantsAutomaticTemperatureTracking = input("Do you want continuous temperature tracking? (Y/N): ")
    if userWantsAutomaticTemperatureTracking.lower == 'y' or userWantsAutomaticTemperatureTracking.lower == 'yes':
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
    APIKey = str(input("Please give API Key for openWeatherMap: "))
    logging.info('User Provided API Key: ' + str(userWantsAutomaticTemperatureTracking))



# Inital setup for the script
userWantsAutomaticTemperatureTracking = True
tempCheckRecurrance = 60
currentDay = str(date.today())
# bus = SMBus(1)
# bme280 = BME280(i2c_dev=bus)
# pms5003 = PMS5003()

APIKey = ''
generateLogFile()
userSurvey()

lat = 40.765031
lon = -111.849385

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