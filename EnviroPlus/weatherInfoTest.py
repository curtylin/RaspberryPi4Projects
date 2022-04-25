import sys
import requests
import json

def getWeather():
    lat = '40.765031'
    lon = '-111.849385'
    URL = 'https://api.openweathermap.org/data/2.5/onecall?lat=' +str(lat) + '&lon=' + str(lon) +  '&appid=' + APIKey + '&units=metric'
    response = requests.get(URL)
    if not response.ok:
        print ('HTTP Response: ' , response.status_code , response.reason)
    responseObj = response.json()
    temperature = responseObj["current"]["temp"]
    weather = responseObj["current"]["weather"][0]["main"]

    alerts = ""
    try:
        alerts = responseObj["alerts"]
    except:
        pass
    return temperature, weather, alerts

print(getWeather())

sys.exit(0)