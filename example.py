import os
import numpy as np
import pandas as pd

from sitka.general.settings import *
from sitka.io.time import *
from sitka.io.weather import *
from sitka.calculations.solar import *
from sitka.components.site import *
import sitka

dir_path = os.getcwd()
weather_file = os.path.join(dir_path, 'USA_WA_Seattle-Boeing.Field.727935_TMY3.epw')

start_hour = 0
end_hour = 8760
time_steps_per_hour = 4


# Simulation run parameters
settings = Settings(dir_path)

time = Time(start_hour=start_hour, end_hour=end_hour, time_steps_per_hour=time_steps_per_hour)

weather = EPW(settings, time, weather_file)
print(weather.location)

# Setup site
site = Site(weather.latitude, weather.longitude, weather.elevation)
print(site.latitude)
print(site.longitude)

# Solar angles
#solar_angles = SolarAngles2(time, site)


# Check solar angles
#print(solar_angles.get_time_series('equation_of_time'))


print(sitka.solar2.calculate_equation_of_time(1))
