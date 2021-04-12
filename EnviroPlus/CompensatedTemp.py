from bme280 import BME280

# Get the temperature of the CPU for compensation
def get_cpu_temperature():
    with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
        temp = f.read()
        temp = int(temp) / 1000.0
    return temp

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus


## Code referenced from CompensatedTemperature.py in EnviroPlus library.
def get_compensated_temperature(factor):
    for i in range(3):
        bus = SMBus(1)
        bme280 = BME280(i2c_dev=bus)
        cpu_temps = [get_cpu_temperature()] * 5

        cpu_temp = get_cpu_temperature()
        # Smooth out with some averaging to decrease jitter
        cpu_temps = cpu_temps[1:] + [cpu_temp]
        avg_cpu_temp = sum(cpu_temps) / float(len(cpu_temps))
        raw_temp = bme280.get_temperature()
        comp_temp = raw_temp - ((avg_cpu_temp - raw_temp) / factor)
    
        if i == 2:
            return comp_temp