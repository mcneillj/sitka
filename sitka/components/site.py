import numpy as np

class Site:
    def __init__(self, latitude=0, longitude=0, elevation=0):
        self.local_standard_meridian = None
        self._latitude = latitude
        self.longitude = longitude
        self.elevation = elevation

        # Run method to update all calculated values
        self.update_calculated_values()

    def update_calculated_values(self):
        self.calculate_local_standard_meridian()

    def calculate_local_standard_meridian(self):
        long = self.longitude
        std_mer = np.sign(long)*np.floor(np.abs(long)/15)*15
        self.local_standard_meridian = std_mer

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        self._latitude = value
        self.update_calculated_values()
