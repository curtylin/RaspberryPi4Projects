# Raspberry Pi 4 Projects
Github repo containing all of my Raspberry Pi projects. 

 ### Authors:
 Curtis Lin

 ### Date of Creation: 
9/23/2020

 # Author Notes: 
 N/A
 
 ---
 ## Auto Weather Logger
 Simple python script can automatically log temperature using Enviro+'s hardware and libraries in Python. User can customize how often temperatures are taken and if they want to only have one temperature check or a continuous one. In addition, it can measure particulates in the air using the PMS5003 sensors. 

 ### Key Features:
 - Particulates: Measures particulates using a PMS5003 sensor port (if plugged into Enviro+, not included in purchase of Enviro+).
 - Default Measurements: Measures Temperature, Humidity, Pressure using included hardware from Enviro+.
 - Single vs Continuous Measurement: Allows for single measuring or continuous measuring over time. 
 - New Log Everyday: Creates new log file with the start of a new day.
 - Customized measuring frequency: user can specify how often a measurement is taken. 
 
 ### How To Use:
  ```bash
pi@RaspberryPi:  python3 AutoWeatherLogger.py
```

---
 ## Utah Humane Society Scraper
 Simple python script can automatically scrape the Utah Humane Society website and outputs the current listings into a simple text file.  

 ### Key Features:
 -  Returns a single listing in a line that includes the following:
 -- Name
 -- Sex
 -- Breed
 -- Weight
 -- Age (in months)
 -- Availability
 -- price
  
 
 ### How To Use:
  ```bash
pi@RaspberryPi:  python3 UtahHumaneSociety.py
```

