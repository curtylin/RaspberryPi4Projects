from datetime import datetime, date
from sense_hat import SenseHat

def logTemperature():
    sense = SenseHat()

    Ptemp = sense.get_temperature_from_pressure()
    Htemp = sense.get_temperature_from_humidity()

    print("Temperature (from thermometer): %s C" % sense.temperature)
    print("Temperature (from pressure): %s C" % Ptemp)
    print("Temperature (from humidity): %s C" % Htemp)

    writeLog.write('[' + str(datetime.now()) + '] Current Temp(from pressure): ' + str(Ptemp) + ' C \n')
    writeLog.write('[' + str(datetime.now()) + '] Current Temp(from humidity): ' + str(Htemp) + ' C \n')


userWantsAutomaticTemperatureTracking = True
tempCheckRecurrance = 60

writeLogFileName = 'AutoTemperatureLog' + str(date.today()) + '.log'
writeLog = open(writeLogFileName, 'w', encoding='cp1252')
writeLog.write('[' + str(datetime.now()) + '] Started AutoTemperature.py script. \n')


userWantsAutomaticTemperatureTracking = input("Do you want continuous temperature tracking? (Y/N): ")
if userWantsAutomatic.lower == 'y' or userWantsAutomatic.lower == 'yes':
    userWantsAutomaticTemperatureTracking = True
    try:
        tempCheckRecurrance = float(input("How often do you want to check temperatures? (in seconds): "))
    except:
        tempCheckRecurrance = float(input("Please give a valid number input in seconds: "))
    writeLog.write('[' + str(datetime.now()) + '] Script taking temperature every ' + str(tempCheckRecurrance) + ' seconds. \n')

else:
    userWantsAutomaticTemperatureTracking = False

writeLog.write('[' + str(datetime.now()) + '] userWantsAutomaticTemperatureTracking: ' + str(userWantsAutomaticTemperatureTracking) + '\n')


if userWantsAutomaticTemperatureTracking:
    while userWantsAutomaticTemperatureTracking:
        logTemperature()
        time.sleep(tempCheckRecurrance)
else:
    logTemperature()

writeLog.close()