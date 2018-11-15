"""Site and building information.
"""
import numpy as np

class Site:
    """
    Represent the building site location and properties.

    Parameters
    ----------
    latitude : float
        Site latitude in degrees.
    longitude : float
        Site longitude in degrees.
    elevation : float
        Site elevation above sea-level in meters.

    Attributes
    ----------
    local_standard_meridian
    latitude
    longitude
    elevation

    Methods
    -------
    update_calculated_values
    calculate_local_standard_meridian

    """
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
        """
        Calculate the local standard meridian based on the site longitude.

        Parameters
        ----------
        longitude

        Yields
        --------
        local_standard_meridian : float
        """
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
