from datetime import datetime, date
import requests
import json

global currentDay, userWantsAutomaticTemperatureTracking, APIKey
global lat, lon

# Inital setup for the script
userWantsAutomaticTemperatureTracking = True
tempCheckFrequency = 5
currentDay = str(date.today())

def print_weather(latitude, longitude):
    global currentHour
    response = requests.get(f"https://api.weather.gov/points/{latitude},{longitude}")
    if not response.ok:
        print ('HTTP Response: ' , response.status_code , response.reason)
        return
    responseObj = response.json()
    
    location_city = responseObj["properties"]["relativeLocation"]["properties"]["city"]
    location_state = responseObj["properties"]["relativeLocation"]["properties"]["state"]
    location_str = f"{location_city}, {location_state}"

    print(datetime.now())
    print(location_str)


    response = requests.get(responseObj["properties"]["forecast"])
    if not response.ok:
        print ('HTTP Response: ' , response.status_code , response.reason)
        return
    response_forecast_Obj = response.json()

    for i in range(4):
        forecast = response_forecast_Obj["properties"]["periods"][i]
        print(f"{forecast['name']}:")
        print(f"    Temperature({forecast['temperatureUnit']})   :   {forecast['temperature']}")
        print(f"    Weather          :   {forecast['shortForecast']}")
        print(f"    Precipitation(%) :   {forecast['probabilityOfPrecipitation']['value']}")
        print("")


    response = requests.get(responseObj["properties"]["forecastHourly"])
    if not response.ok:
        print ('HTTP Response: ' , response.status_code , response.reason)
        return
    response_forecast_hourly_Obj = response.json()
    print("Forecast Hourly: ")
    for i in range(3):
        forecast = response_forecast_hourly_Obj["properties"]["periods"][i]
        print(forecast["startTime"])
        print(f"    Temperature({forecast['temperatureUnit']})   :   {forecast['temperature']}")
        print(f"    Weather          :   {forecast['shortForecast']}")
        print(f"    Precipitation(%) :   {forecast['probabilityOfPrecipitation']['value']}")





    response = requests.get(f"https://api.weather.gov/alerts/active?point={latitude}%2C{longitude}")
    responseObj = response.json()
    if not response.ok:
        print ('HTTP Response: ' , response.status_code , response.reason)
        return
    for i in range(len(responseObj["features"])):
        if i == 0:
            print(responseObj["title"])
        alert = responseObj["features"][i]
        print(f"{alert['properties']['event']}:")
        print(f"    {alert['properties']['headline']}")
        print(f"    severity   :    {alert['properties']['severity']}")
        print(f"    urgency    :    {alert['properties']['urgency']}")
        print(f"    certainty  :    {alert['properties']['certainty']}")
        print(f"{alert['properties']['description']}")
        print(f"")
    

lat, lon = 45.420345, -122.718759

print_weather(latitude=lat, longitude=lon)