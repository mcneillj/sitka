"""Radiation models (external shortwave, external longwave).
"""
import numpy as np
import pandas as pd

from sitka.utils.time_series import TimeSeriesComponent


class ExternalShortwaveRadiation(TimeSeriesComponent):
    """
    External shortwave radiation calculation for time-series.

    Parameters
    ----------
    time : Time
    solar_angles : SolarAngles
    weather : Weather
    surface : Surface
    surface_solar_angles : SurfaceSolarAngles

    Attributes
    ----------
    ratio_of_clear_sky_diffuse_on_horizontal_to_tilted : Series
        Ratio of clear sky diffuse radiation on a horizontal surface to the
        clear sky diffuse radiation on a tilted surface [0-1].
    incident_direct_radiation : Series
        Incident direct solar radiation on surface [W-m^2].
    incident_diffuse_radiation : Series
        Incident diffuse solar radiation on surface [W-m^2].
    incident_reflected_radiation : Series
        Incident reflected solar radiation on surface [W-m^2].
    incident_total_radiation : Series
        Incident total solar radiation on surface [W-m^2].
    incident_total_heat_flux : Series
        Incident total heat flux on surface [W-m^2].
    ground_reflectance : float
        Ground reflectance [0-1] default 0.2.
    absorptivity : float
        Surface absorptivity [0-1] default 0.8.
    time : Time
    solar_angles : SolarAngles
    weather : Weather
    surface : Surface
    surface_solar_angles : SurfaceSolarAngles
    """
    def __init__(self, time, solar_angles, weather, surface, surface_solar_angles):
        # General properties
        self.ratio_of_clear_sky_diffuse_on_horizontal_to_tilted = None

        # Incident solar radiation
        self.incident_direct_radiation = None
        self.incident_diffuse_radiation = None
        self.incident_reflected_radiation = None
        self.incident_total_radiation = None
        self.incident_total_heat_flux = None

        # Associated objects
        self._solar_angles = solar_angles
        self._weather = weather
        self._surface = surface
        self._surface_solar_angles = surface_solar_angles

        # General Parameters
        self.ground_reflectance = 0.2  # Ground reflectance []
        self.absorptivity = 0.8  # Surface absorptivity []

        # Add attributes from super class
        super().__init__(time)

        # Run method to update all calculated values
        self.update_calculated_values()

    def update_calculated_values(self):
        print('Updating external shortwave radiation calculations.')
        self.calculate_ratio_of_clear_sky_diffuse_on_horizontal_to_tilted()
        self.calculate_incident_direct_radiation()
        self.calculate_incident_diffuse_radiation()
        self.calculate_incident_reflected_radiation()
        self.calculate_incident_total_radiation()
        self.calculate_incident_total_heat_flux()

    def calculate_ratio_of_clear_sky_diffuse_on_horizontal_to_tilted(self):
        """
        Calculate the ratio of clear sky diffuse radiation on a horizontal
        surface to a tilted surface for each item in the series.

        Yields
        ----------
        ratio_of_clear_sky_diffuse_on_horizontal_to_tilted : Series

        References
        --------
        """
        cos_incidence_angle = np.cos(np.deg2rad(self.surface_solar_angles.incidence_angle))
        Y = 0.55+0.437*cos_incidence_angle+0.313*cos_incidence_angle**2
        Y[Y<0.45] = 0.45
        self.ratio_of_clear_sky_diffuse_on_horizontal_to_tilted = pd.Series(Y)

    def calculate_incident_direct_radiation(self):
        """
        Calculate the incident direct solar radiation on surface for each
        item in the series.

        Yields
        ----------
        incident_direct_radiation : Series

        References
        --------
        """
        sun_on_surface = self.surface_solar_angles.sun_on_surface.astype(float)
        incidence_angle = np.deg2rad(self.surface_solar_angles.incidence_angle)
        direct_normal_radiation = self.weather.direct_normal_radiation
        incident_direct_radiation = direct_normal_radiation*np.cos(incidence_angle)
        incident_direct_radiation[sun_on_surface == 0] = 0.0
        incident_direct_radiation[np.cos(incidence_angle) < 0] = 0.0
        self.incident_direct_radiation = pd.Series(incident_direct_radiation)

    def calculate_incident_diffuse_radiation(self):
        """
        Calculate the incident diffuse solar radiation on surface for each
        item in the series.

        Yields
        ----------
        incident_diffuse_radiation : Series

        References
        --------
        """
        incidence_angle = np.deg2rad(self.surface_solar_angles.incidence_angle)
        rad_surface_tilt = np.deg2rad(self.surface.tilt)
        diffuse_horizontal_radiation = self.weather.diffuse_horizontal_radiation
        Y = self.ratio_of_clear_sky_diffuse_on_horizontal_to_tilted
        if self.surface.tilt<=90:
            incident_diffuse_radiation = diffuse_horizontal_radiation*(Y*np.sin(rad_surface_tilt)+np.cos(rad_surface_tilt))
        else:
            incident_diffuse_radiation = diffuse_horizontal_radiation*Y*np.sin(rad_surface_tilt)

        self.incident_diffuse_radiation = pd.Series(incident_diffuse_radiation)

    def calculate_incident_reflected_radiation(self):
        """
        Calculate the incident reflected solar radiation on surface for each
        item in the series.

        Yields
        ----------
        incident_reflected_radiation : Series

        References
        --------
        """
        ground_reflectance = self.ground_reflectance
        direct_solar_radiation = self.weather.direct_normal_radiation
        diffuse_solar_radiation = self.weather.diffuse_horizontal_radiation
        rad_solar_altitude = np.deg2rad(self.solar_angles.solar_altitude)
        rad_surface_tilt = np.deg2rad(self.surface.tilt)
        incident_reflected_radiation = ground_reflectance*(direct_solar_radiation*np.sin(rad_solar_altitude)+diffuse_solar_radiation)*(1-np.cos(rad_surface_tilt))
        self.incident_reflected_radiation = pd.Series(incident_reflected_radiation)

    def calculate_incident_total_radiation(self):
        """
        Calculate the incident total solar radiation on surface for each
        item in the series.

        Yields
        ----------
        incident_total_radiation : Series

        References
        --------
        """
        incident_direct_radiation = self.incident_direct_radiation
        incident_diffuse_radiation = self.incident_diffuse_radiation
        incident_reflected_radiation = self.incident_reflected_radiation
        incident_total_radiation = incident_direct_radiation + incident_diffuse_radiation + incident_reflected_radiation
        self.incident_total_radiation = pd.Series(incident_total_radiation)

    def calculate_incident_total_heat_flux(self):
        """
        Calculate the incident total heat flux on surface for each
        item in the series.

        Yields
        ----------
        incident_total_heat_flux : Series

        References
        --------
        """
        absorptivity = self.absorptivity
        incident_total_radiation = self.incident_total_radiation
        incident_total_heat_flux = absorptivity*incident_total_radiation
        self.incident_total_heat_flux = pd.Series(incident_total_heat_flux)

    @property
    def solar_angles(self):
        return self._solar_angles

    @solar_angles.setter
    def solar_angles(self, value):
        self._solar_angles = value
        self.update_calculated_values()

    @property
    def weather(self):
        return self._weather

    @weather.setter
    def weather(self, value):
        self._weather = value
        self.update_calculated_values()

    @property
    def surface(self):
        return self._surface

    @surface.setter
    def surface(self, value):
        self._surface= value
        self.update_calculated_values()

    @property
    def surface_solar_angles(self):
        return self._surface_solar_angles

    @surface_solar_angles.setter
    def surface_solar_angles(self, value):
        self._surface_solar_angles= value
        self.update_calculated_values()


class ExternalLongwaveRadiation(TimeSeriesComponent):
    """
    External longwave radiation calculation for time-series.

    Parameters
    ----------
    time : Time
    weather : Weather
    surface : Surface
    surface_temperature : Series

    Attributes
    ----------
    sigma : float
        Stefan-Boltzmann constant.
    absorptivity : float
        Surface material thermal radiation absorptivity.
    horizontal_infrared_radiation_sky : Series
    surface_temperature : Series
    ambient_temperature : Series
    sky_temperature : Series
    ground_view_factor : float
    sky_view_factor : float
    air_view_factor : float
    ground_radiative_heat_transfer : Series
    sky_radiative_heat_transfer : Series
    air_radiative_heat_transfer : Series
    total_radiative_heat_transfer : Series
    time : Time
    weather : Weather
    surface : Surface
    """
    def __init__(self, time, weather, surface, surface_temperature):
        # Radiation parameters
        self.sigma = 5.67e-8  # stephan-boltzmann constant
        self.absorptivity = 0.90

        # View factors
        self.ground_view_factor = None
        self.sky_view_factor = None
        self.air_view_factor = None

        # Thermal properties
        self.surface_temperature = surface_temperature

        # Heat transfer components
        self.ground_radiation = None
        self.sky_radiation = None
        self.air_radiation = None
        self.total_radiation = None

        # Associated objects
        self._weather = weather
        self._surface = surface

        # Add attributes from super class
        super().__init__(time)

        # Run method to update all calculated values
        self.update_calculated_values()

    def update_calculated_values(self):
        print('Updating external longwave radiation calculations.')
        self.calculate_ground_view_factor()
        self.calculate_sky_view_factor()
        self.calculate_air_view_factor()
        self.calculate_ground_long_wave_radiation()
        self.calculate_sky_long_wave_radiation()
        self.calculate_air_long_wave_radiation()
        self.calculate_total_long_wave_radiation()

    def calculate_ground_view_factor(self):
        """
        Calculate the view factor between the ground and the surface.

        Yields
        ----------
        ground_view_factor : float

        References
        --------
        """
        rad_surface_tilt = np.deg2rad(self.surface.tilt)
        ground_view_factor = 0.5*(1-np.cos(rad_surface_tilt))
        self.ground_view_factor = ground_view_factor

    def calculate_sky_view_factor(self):
        """
        Calculate the view factor between the sky and the surface.

        Yields
        ----------
        sky_view_factor : float

        References
        --------
        """
        rad_surface_tilt = np.deg2rad(self.surface.tilt)
        sky_view_factor = 0.5*(1+np.cos(rad_surface_tilt))
        self.sky_view_factor = sky_view_factor

    def calculate_air_view_factor(self):
        """
        Calculate the view factor between the air and the surface.

        Yields
        ----------
        sky_view_factor : float

        References
        --------
        """
        self.air_view_factor = 1

    def calculate_ground_long_wave_radiation(self):
        """
        Calculate the long wave radiation from the surface to the ground for
        each item in the series.

        Yields
        ----------
        ground_radiative_heat_transfer : Series

        References
        --------
        """
        amb_temp = self.weather.dry_bulb_temperature
        abs_amb_temp = amb_temp+273
        surf_temp = self.surface_temperature
        abs_surf_temp = self.surface_temperature+273

        # initialize array
        hrgnd = pd.Series(np.zeros(self.time.length))
        hrgnd[amb_temp != surf_temp] = self.absorptivity*self.sigma*self.ground_view_factor*((abs_amb_temp)**4-(abs_surf_temp)**4)/(amb_temp-surf_temp)
        self.ground_radiation = pd.Series(hrgnd)

    def calculate_sky_long_wave_radiation(self):
        """
        Calculate the long wave radiation from the surface to the sky for
        each item in the series.

        Yields
        ----------
        sky_long_wave_radiation : Series

        References
        --------
        """
        sky_temp = self.weather.sky_temperature
        abs_sky_temp = self.weather.sky_temperature+273
        surf_temp = self.surface_temperature
        abs_surf_temp = self.surface_temperature+273

        # initialize array
        hrsky = pd.Series(np.zeros(self.time.length))
        hrsky[sky_temp != surf_temp] = self.absorptivity*self.sigma*self.sky_view_factor*((abs_sky_temp)**4-(abs_surf_temp)**4)/(sky_temp-surf_temp)
        self.sky_radiation = pd.Series(hrsky)

    def calculate_air_long_wave_radiation(self):
        """
        Calculate the long wave radiation from the surface to the air for
        each item in the series.

        Yields
        ----------
        air_long_wave_radiation : Series

        References
        --------
        """
        amb_temp = self.weather.dry_bulb_temperature
        abs_amb_temp = self.weather.dry_bulb_temperature+273
        surf_temp = self.surface_temperature
        abs_surf_temp = self.surface_temperature+273

        # initialize array

        hrair = pd.Series(np.zeros(self.time.length))
        hrair[amb_temp != surf_temp] = self.absorptivity*self.sigma*self.air_view_factor*((abs_amb_temp)**4-(abs_surf_temp)**4)/(amb_temp-surf_temp)
        self.air_radiation = pd.Series(hrair)

    def calculate_total_long_wave_radiation(self):
        """
        Calculate the total long wave radiation from the surface for
        each item in the series.

        Yields
        ----------
        total_radiation : Series

        References
        --------
        """
        total_radiation = self.ground_radiation + self.sky_radiation + self.air_radiation
        self.total_radiation = pd.Series(total_radiation)


    @property
    def weather(self):
        return self._weather

    @weather.setter
    def weather(self, value):
        self._weather = value
        self.update_calculated_values()

    @property
    def surface(self):
        return self._surface

    @surface.setter
    def surface(self, value):
        self._surface= value
        self.update_calculated_values()
