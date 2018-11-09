class TimeSeriesComponent:
    def __init__(self, time):
        # General Properties
        self._time = time

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        self._time = value
        self.update_calculated_values()

    def get_time_series(self, parameter):
        series = getattr(self, parameter)
        series.index = self.time.datetime_range

        return series
