from datetime import datetime, date
import logging
import time
import requests
import json

global currentDay, userWantsAutomaticTemperatureTracking
global lat, lon

# Inital setup for the script
userWantsAutomaticTemperatureTracking = True
tempCheckFrequency = 60
currentDay = str(date.today())

def logWeather():
    URL = 'https://api.openweathermap.org/data/2.5/onecall?lat=' +str(lat) + '&lon=' + str(lon) +  '&appid=' + APIKey + '&units=metric'
    response = requests.get(URL)
    if not response.ok:
        print ('HTTP Response: ' , response.status_code , response.reason)
    responseObj = response.json()
    
    temperature = responseObj["current"]["temp"]
    pressure = responseObj["current"]["pressure"]
    humidity = responseObj["current"]["humidity"]
    weather = responseObj["current"]["weather"]["description"]

    print('[' + str(datetime.now()) + '] \tTemperature (*C): ' + str(temperature) + '\tPressure (hPa): ' + str(pressure) + '\tHumidity (%): ' + str(humidity) + '\n')
    logging.info(str(temperature) + '\t\t\t\t' + str(pressure) + '\t\t\t' +  str(humidity))

def generateLogFile():
    logging.basicConfig(format='%(asctime)s: %(message)s', filename='AutoWeatherLog' + str(date.today()) + '.log', level=logging.INFO)
    logging.info('Started logging from script.')
    logging.info('Temperature (*C): \t Pressure (hPa): \t Humidity (%): ')

def userSurvey():
    global tempCheckFrequency, userWantsAutomaticTemperatureTracking, APIKey
    userWantsAutomaticTemperatureTracking = input("Do you want continuous temperature tracking? (Y/N): ")
    if userWantsAutomaticTemperatureTracking.lower() == 'y' or userWantsAutomaticTemperatureTracking.lower() == 'yes':
        userWantsAutomaticTemperatureTracking = True
        try:
            tempCheckFrequency = float(input("How often do you want to check temperatures? (in seconds): "))
        except:
            tempCheckFrequency = float(input("Please give a valid number input in seconds: "))
            logging.info('Script taking info every ' + str(tempCheckFrequency) + ' seconds.')
    else:
        userWantsAutomaticTemperatureTracking = False
        logging.info('userWantsAutomaticTemperatureTracking: ' + str(userWantsAutomaticTemperatureTracking))
    APIKey = str(input("Please give API Key for openWeatherMap: "))
    logging.info('User Provided API Key: ' + str(APIKey))



APIKey = ''
generateLogFile()
userSurvey()

lat = '40.765031'
lon = '-111.849385'

if userWantsAutomaticTemperatureTracking:
    while userWantsAutomaticTemperatureTracking:
        if currentDay != str(date.today()):     #Script automatically generates a new log file at the start of a new day.
            logging.FileHandler.close()
            generateLogFile()
        logWeather()
        time.sleep(tempCheckFrequency)
else:
    logWeather()

logging.FileHandler.close()
logging.shutdown()
