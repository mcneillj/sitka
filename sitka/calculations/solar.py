"""Solar geometry, angles and shading.
"""
import numpy as np
import pandas as pd

from sitka.utils.time_series import TimeSeriesComponent

class SolarAngles(TimeSeriesComponent):
    """
    Store solar angles for a site.

    Parameters
    ----------
    time
    site

    Attributes
    ----------
    gamma : Series
        Gamma angle.
    equation_of_time: Series
        Equation of time.
    apparent_solar_time: Series
        Apparent solar time.
    declination: Series
        Solar declination angle.
    hour_angle: Series
        Hour angle of the sun.
    number_of_sunlight_hours: Series
        Number of sunlight hours per day.
    sun_up: Series
        Flag to define when the sun is above the
        horizon (1 = sun up, 0 = sun is down).
    solar_zenith: Series
        Solar zenith angle.
    solar_altitude: Series
        Solar altitude angle.
    solar_azimuth: Series
        Solar azimuth angle.
    """
    def __init__(self, time, site):
        # Solar angles
        self.gamma = None
        self.equation_of_time = None
        self.apparent_solar_time = None
        self.declination = None
        self.hour_angle = None
        self.sunrise_hour_angle = None
        self.sunset_hour_angle = None
        self.number_of_sunlight_hours = None
        self.sun_up = None
        self.solar_zenith = None
        self.solar_altitude = None
        self.solar_azimuth = None

        # General Properties
        self._site = site

        # Add attributes from super class
        super().__init__(time)

        # Run method to update all calculated values
        self.update_calculated_values()

    def update_calculated_values(self):
        """Update all calculated values.

        """
        print('Updating solar angles')
        self.calculate_gamma()
        self.calculate_equation_of_time()
        self.calculate_apparent_solar_time()
        self.calculate_declination()
        self.calculate_hour_angle()
        self.calculate_sunrise_hour_angle()
        self.calculate_sunset_hour_angle()
        self.calculate_number_of_sunlight_hours()
        self.calculate_sun_up()
        self.calculate_solar_zenith()
        self.calculate_solar_altitude()
        self.calculate_solar_azimuth()

    def calculate_gamma(self):
        """
        Calculate Gamma from the julian_day.

        Parameters
        ----------
        julian_day : Series
            Julian day number [1-365]

        Yields
        --------
        gamma : Series

        References
        --------
        """
        gamma = 360*(self.time.julian_day-1)/365
        self.gamma = pd.Series(gamma)

    def calculate_equation_of_time(self):
        """
        Calculate equation of time from Gamma.

        Parameters
        ----------
        gamma : Series

        Yields
        --------
        equation_of_time : Series

        References
        --------
        """
        gamma = self.gamma
        cosgamma = np.cos(np.deg2rad(gamma))
        singamma = np.sin(np.deg2rad(gamma))
        cos2gamma = np.cos(np.deg2rad(2*gamma))
        sin2gamma = np.sin(np.deg2rad(2*gamma))
        equation_of_time = 2.2918*(0.0075+0.1868*cosgamma-3.2077*singamma-1.4615*cos2gamma-4.089*sin2gamma)
        self.equation_of_time = pd.Series(equation_of_time)

    def calculate_apparent_solar_time(self):
        """
        Calculate the apparent solar time for each item in the series.

        Parameters
        ----------
        hour : Series
        equation_of_time : Series
        longitude : float
        local_standard_meridian : float

        Yields
        ----------
        apparent_solar_time : Series

        References
        --------
        """
        hr = self.time.datetime_range.hour
        apparent_solar_time = hr + self.equation_of_time/60 + (self.site.longitude-self.site.local_standard_meridian)/15
        self.apparent_solar_time = pd.Series(apparent_solar_time)

    def calculate_declination(self):
        """
        Calculate the solar declination angle for each item in the series.

        Parameters
        ----------
        julian_day : Series

        Yields
        ----------
        declination : Series

        References
        --------
        """
        declination =  23.45*(np.sin(np.deg2rad(360*(self.time.julian_day+284)/365)))
        self.declination = pd.Series(declination)

    def calculate_hour_angle(self):
        """
        Calculate the solar hour angle for each item in the series.

        Parameters
        ----------
        apparent_solar_time : Series

        Yields
        ----------
        hour_angle : Series

        References
        --------
        """
        hour_angle = 15*(self.apparent_solar_time-12)
        self.hour_angle = pd.Series(hour_angle)

    def calculate_sunrise_hour_angle(self):
        """
        Calculate the sunrise hour angle for each item in the series.

        Parameters
        ----------
        latitude : float
        declination : Series

        Yields
        ----------
        sunrise_hour_angle : Series

        References
        --------
        """
        sunrise_hour_angle = -np.rad2deg(np.arccos(-np.tan(np.deg2rad(self.site.latitude))*np.tan(np.deg2rad(self.declination))))
        self.sunrise_hour_angle = pd.Series(sunrise_hour_angle)

    def calculate_sunset_hour_angle(self):
        """
        Calculate the sunset hour angle for each item in the series.

        Parameters
        ----------
        latitude : float
        declination : Series

        Yields
        ----------
        sunset_hour_angle : Series

        References
        --------
        """
        sunset_hour_angle = np.rad2deg(np.arccos(-np.tan(np.deg2rad(self.site.latitude))*np.tan(np.deg2rad(self.declination))))
        self.sunset_hour_angle = pd.Series(sunset_hour_angle)

    def calculate_number_of_sunlight_hours(self):
        """
        Calculate the number of sunlight hours per day for each item in the series.

        Parameters
        ----------
        latitude : float
        declination : Series

        Yields
        ----------
        number_of_sunlight_hours : Series

        References
        --------
        """
        number_of_sunlight_hours = 2/15*np.rad2deg(np.arccos(-np.tan(np.deg2rad(self.site.latitude))*np.tan(np.deg2rad(self.declination))))
        self.number_of_sunlight_hours = pd.Series(number_of_sunlight_hours)

    def calculate_sun_up(self):
        """
        Set a flag for whether the sun is above the horizon for each item in the series.

        Parameters
        ----------
        hour_angle : Series
        sunrise_hour_angle : Series
        sunset_hour_angle : Series

        Yields
        ----------
        sun_up : Series

        References
        --------
        """
        sun_up = np.ones(self.time.length)*False
        sun_up[
            (self.hour_angle > self.sunrise_hour_angle) &
            (self.hour_angle < self.sunset_hour_angle)
        ] = True

        self.sun_up = pd.Series(sun_up)

    def calculate_solar_zenith(self):
        """
        Calculate the solar zenith angle for each item in the series.

        Parameters
        ----------
        latitude : float
        sun_up : Series
        declination : Series
        hour_angle : Series

        Yields
        ----------
        solar_zenith : Series

        References
        --------
        """
        sun_up = self.sun_up
        latitude = np.deg2rad(self.site.latitude)
        declination = np.deg2rad(self.declination)
        hour_angle = np.deg2rad(self.hour_angle)
        solar_zenith = sun_up*np.rad2deg(np.arccos(np.cos(latitude)*np.cos(declination)*np.cos(hour_angle)+np.sin(latitude)*np.sin(declination)))
        self.solar_zenith = pd.Series(solar_zenith)

    def calculate_solar_altitude(self):
        """
        Calculate the solar altitude angle for each item in the series.

        Parameters
        ----------
        calculate_sun_up : Series
        solar_zenith : Series

        Yields
        ----------
        solar_altitude : Series

        References
        --------
        """
        sun_up = self.sun_up
        solar_zenith = self.solar_zenith
        solar_altitude = sun_up*(90-solar_zenith)
        self.solar_altitude = pd.Series(solar_altitude)

    def calculate_solar_azimuth(self):
        """
        Calculate the solar azimuth angle for each item in the series.

        Parameters
        ----------
        latitude : float
        declination : Series
        hour_angle : Series
        solar_altitude : Series

        Yields
        ----------
        solar_azimuth : Series

        References
        --------
        """
        rad_latitude = np.deg2rad(self.site.latitude)
        rad_declination = np.deg2rad(self.declination)
        rad_hour_angle = np.deg2rad(self.hour_angle)
        rad_solar_altitude = np.deg2rad(self.solar_altitude)
        rad_solar_azimuth = np.arcsin(np.sin(rad_hour_angle)*np.cos(rad_declination)/np.cos(rad_solar_altitude))  #azimuth = 0 is due south
        solar_azimuth = np.rad2deg(rad_solar_azimuth)
        self.solar_azimuth = pd.Series(solar_azimuth)

    @property
    def site(self):
        return self._site

    @site.setter
    def site(self, value):
        self._site= value
        self.update_calculated_values()
