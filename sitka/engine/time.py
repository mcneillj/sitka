import numpy as np
import pandas as pd

# TODO Get start and stop times from settings

class Time:
    def __init__(self, year=pd.datetime.now().year, start_hour=0, end_hour=8760, time_steps_per_hour=4):
        self.time_range = None
        self.datetime_range = None
        self.time_step = None
        self.length = None
        self.julian_day = None
        self._year = year
        self._start_hour = start_hour
        self._end_hour = end_hour
        self._time_steps_per_hour = time_steps_per_hour

        # Run method to update all calculated values
        self.update_calculated_values()

    def update_calculated_values(self):
        print('Updating time object')
        self.calculate_time_step()
        self.calculate_time_range()
        self.calculate_datetime_range()
        self.calculate_julian_day()

    def calculate_time_step(self):
        self.time_step = 3600/self.time_steps_per_hour  # time step [s]

    def calculate_time_range(self):
        start_hour = self.start_hour*3600
        end_hour = self.end_hour*3600
        dt = self.time_step
        time_range = np.linspace(start_hour,end_hour,end_hour/dt)
        self.time_range = time_range
        self.length = len(time_range)

    def calculate_datetime_range(self):
        date_str = '1/1/%d 00:00:00' % self.year
        start = pd.to_datetime(date_str) + pd.Timedelta(hours=self.start_hour)
        hourly_periods = (self.end_hour-self.start_hour)*self.time_steps_per_hour
        frequency = str(60/self.time_steps_per_hour) + ' T'
        datetime_range = pd.date_range(start, periods=hourly_periods, freq=frequency)
        self.datetime_range = datetime_range

    def calculate_julian_day(self):
        julian_day = self.datetime_range.dayofyear
        self.julian_day = julian_day

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, value):
        self._year = value
        self.update_calculated_values()

    @property
    def start_hour(self):
        return self._start_hour

    @start_hour.setter
    def start_hour(self, value):
        self._start_hour = value
        self.update_calculated_values()

    @property
    def end_hour(self):
        return self._end_hour

    @end_hour.setter
    def end_hour(self, value):
        self._end_hour = value
        self.update_calculated_values()

    @property
    def time_steps_per_hour(self):
        return self._time_steps_per_hour

    @time_steps_per_hour.setter
    def time_steps_per_hour(self, value):
        self._time_steps_per_hour = value
        self.update_calculated_values()
