import numpy as np
import pandas as pd

from sitka.utils.time_series import TimeSeriesComponent

class SolarAngles(TimeSeriesComponent):
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
        self.air_mass = None

        # General Properties
        self._site = site

        # Add attributes from super class
        super().__init__(time)

        # Run method to update all calculated values
        self.update_calculated_values()

    def update_calculated_values(self):
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
        self.calculate_air_mass()

    def calculate_gamma(self):
        gamma = 360*(self.time.julian_day-1)/365
        self.gamma = pd.Series(gamma) #pd.Series(gamma)

    def calculate_equation_of_time(self):
        gamma = self.gamma
        cosgamma = np.cos(np.deg2rad(gamma))
        singamma = np.sin(np.deg2rad(gamma))
        cos2gamma = np.cos(np.deg2rad(2*gamma))
        sin2gamma = np.sin(np.deg2rad(2*gamma))
        equation_of_time = 2.2918*(0.0075+0.1868*cosgamma-3.2077*singamma-1.4615*cos2gamma-4.089*sin2gamma)
        self.equation_of_time = pd.Series(equation_of_time)

    def calculate_apparent_solar_time(self):
        hr = self.time.datetime_range.hour
        apparent_solar_time = hr + self.equation_of_time/60 + (self.site.longitude-self.site.local_standard_meridian)/15
        self.apparent_solar_time = pd.Series(apparent_solar_time)

    def calculate_declination(self):
        declination =  23.45*(np.sin(np.deg2rad(360*(self.time.julian_day+284)/365)))
        self.declination = pd.Series(declination)

    def calculate_hour_angle(self):
        hour_angle = 15*(self.apparent_solar_time-12)
        self.hour_angle = pd.Series(hour_angle)

    def calculate_sunrise_hour_angle(self):
        sunrise_hour_angle = -np.rad2deg(np.arccos(-np.tan(np.deg2rad(self.site.latitude))*np.tan(np.deg2rad(self.declination))))
        self.sunrise_hour_angle = pd.Series(sunrise_hour_angle)

    def calculate_sunset_hour_angle(self):
        sunset_hour_angle = np.rad2deg(np.arccos(-np.tan(np.deg2rad(self.site.latitude))*np.tan(np.deg2rad(self.declination))))
        self.sunset_hour_angle = pd.Series(sunset_hour_angle)

    def calculate_number_of_sunlight_hours(self):
        number_of_sunlight_hours = 2/15*np.rad2deg(np.arccos(-np.tan(np.deg2rad(self.site.latitude))*np.tan(np.deg2rad(self.declination))))
        self.number_of_sunlight_hours = pd.Series(number_of_sunlight_hours)

    def calculate_sun_up(self):
        ## TODO partial hours
        sun_up = np.ones(self.time.length)*False
        sun_up[
            (self.hour_angle > self.sunrise_hour_angle) &
            (self.hour_angle < self.sunset_hour_angle)
        ] = True

        self.sun_up = pd.Series(sun_up)

    def calculate_solar_zenith(self):
        sun_up = self.sun_up
        latitude = np.deg2rad(self.site.latitude)
        declination = np.deg2rad(self.declination)
        hour_angle = np.deg2rad(self.hour_angle)
        solar_zenith = sun_up*np.rad2deg(np.arccos(np.cos(latitude)*np.cos(declination)*np.cos(hour_angle)+np.sin(latitude)*np.sin(declination)))
        self.solar_zenith = pd.Series(solar_zenith)

    def calculate_solar_altitude(self):
        #rad_latitude = np.deg2rad(self.site.latitude)
        #rad_declination = np.deg2rad(self.declination)
        #rad_hour_angle = np.deg2rad(self.hour_angle)
        #rad_solar_altitude = np.arcsin(np.cos(rad_latitude)*np.cos(rad_declination)*np.cos(rad_hour_angle)+np.sin(rad_latitude)*np.sin(rad_declination))
        #solar_altitude = np.rad2deg(rad_solar_altitude)
        #solar_altitude[solar_altitude<0] = 0
        sun_up = self.sun_up
        solar_zenith = self.solar_zenith
        solar_altitude = sun_up*(90-solar_zenith)
        self.solar_altitude = pd.Series(solar_altitude)

    def calculate_solar_azimuth(self):
        rad_latitude = np.deg2rad(self.site.latitude)
        rad_declination = np.deg2rad(self.declination)
        rad_hour_angle = np.deg2rad(self.hour_angle)
        rad_solar_altitude = np.deg2rad(self.solar_altitude)
        rad_solar_azimuth = np.arcsin(np.sin(rad_hour_angle)*np.cos(rad_declination)/np.cos(rad_solar_altitude))  #azimuth = 0 is due south
        solar_azimuth = np.rad2deg(rad_solar_azimuth)
        self.solar_azimuth = pd.Series(solar_azimuth)

    def calculate_air_mass(self):
        # Air mass [M]
        sun_up = self.sun_up
        solar_zenith = self.solar_zenith
        air_mass = sun_up*1/np.cos(np.deg2rad(solar_zenith))
        self.air_mass = pd.Series(air_mass)

    @property
    def site(self):
        return self._site

    @site.setter
    def site(self, value):
        self._site= value
        self.update_calculated_values()


class SurfaceSolarAngles:
    def __init__(self, name, time, solar_angles, surface):
        # General properties
        self.name = name
        self.sun_surface_azimuth = None
        self.incidence_angle = None
        self.sun_on_surface = None
        self.profile_angle = None

        # Associated objects
        self._time = time
        self._surface = surface
        self._solar_angles = solar_angles

        # Run method to update all calculated values
        self.update_calculated_values()

    def update_calculated_values(self):
        print('Updating surface solar calculations for ' + self.name)
        self.calculate_sun_surface_azimuth()  # Sun-surface azimuth angle [deg]
        self.calculate_sun_on_surface()  # Times where surface is sunlit [date-time]
        self.calculate_incidence_angle()  # Sun-surface incidence angle [deg]
        self.calculate_profile_angle()

    def calculate_sun_surface_azimuth(self):
        surface_azimuth = np.ones(self.time.length)*self.surface.azimuth
        solar_azimuth = self.solar_angles.solar_azimuth
        sun_surface_azimuth = np.abs(surface_azimuth - solar_azimuth)
        self.sun_surface_azimuth = pd.Series(sun_surface_azimuth, index=self.time.datetime_range)

    def calculate_sun_on_surface(self):
        sun_on_surface = False*np.ones(self.time.length)
        sun_on_surface[
            (self.solar_angles.solar_altitude > 0) &
            (self.sun_surface_azimuth < 90) &
            (self.sun_surface_azimuth > -90)
        ] = True
        self.sun_on_surface = pd.Series(sun_on_surface, index=self.time.datetime_range)

    def calculate_incidence_angle(self):
        sun_on_surface = self.sun_on_surface
        latitude = np.deg2rad(self.solar_angles.site.latitude)
        declination = np.deg2rad(self.solar_angles.declination)
        hour_angle = np.deg2rad(self.solar_angles.hour_angle)
        solar_altitude = np.deg2rad(self.solar_angles.solar_altitude)
        surface_tilt = np.deg2rad(self.surface.tilt)
        surface_azimuth = np.deg2rad(self.surface.azimuth)
        sun_surface_azimuth = np.deg2rad(self.sun_surface_azimuth)
        incidence_angle = np.rad2deg(np.arccos(np.cos(solar_altitude)*np.cos(sun_surface_azimuth)*np.sin(surface_tilt)+np.sin(solar_altitude)*np.cos(surface_tilt)))
        """
        term1 = np.sin(declination)*np.sin(latitude)*np.cos(surface_tilt)
        term2 = np.sin(declination)*np.cos(latitude)*np.sin(surface_tilt)*np.cos(surface_azimuth)
        term3 = np.cos(declination)*np.cos(latitude)*np.cos(surface_tilt)*np.cos(hour_angle)
        term4 = np.cos(declination)*np.sin(latitude)*np.sin(surface_tilt)*np.cos(surface_azimuth)*np.cos(hour_angle)
        term5 = np.cos(declination)*np.sin(surface_tilt)*np.sin(surface_azimuth)*np.sin(hour_angle)
        incidence_angle = np.rad2deg(np.arccos(term1-term2+term3+term4+term5))
        """
        self.incidence_angle = pd.Series(incidence_angle, index=self.time.datetime_range)

    def calculate_profile_angle(self):
        sun_on_surface = self.sun_on_surface
        solar_altitude = np.deg2rad(self.solar_angles.solar_altitude)
        sun_surface_azimuth = np.deg2rad(self.sun_surface_azimuth)
        profile_angle = np.rad2deg(np.arctan(np.tan(solar_altitude)/(np.cos(sun_surface_azimuth))))
        self.profile_angle = pd.Series(profile_angle, index=self.time.datetime_range)

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        self._time = value
        self.update_calculated_values()

    @property
    def surface(self):
        return self._surface

    @surface.setter
    def surface(self, value):
        self._surface= value
        self.update_calculated_values()

    @property
    def solar_angles(self):
        return self._solar_angles

    @solar_angles.setter
    def solar_angles(self, value):
        self._solar_angles = value
        self.update_calculated_values()
