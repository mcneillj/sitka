"""Super classes to attach time series attributes to base classes.
"""
class TimeSeriesComponent:
    """
    Component to attach the date-time object to a Pandas series attribute.

    ...

    Parameters
    ----------
    time : Time object

    Attributes
    ----------
    _time

    Methods
    -------
    update_calculated_values

    """
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
