import numpy as np
import pandas as pd

from sitka.utils.time_series import TimeSeriesComponent


class ExternalShortwaveRadiation(TimeSeriesComponent):
    def __init__(self, name, time, solar_angles, weather, surface):
        # General properties
        self.name = name
        self.ratio_of_clear_sky_diffuse_on_horizontal_to_tilted = None

        # Incident solar radiation
        self.incident_direct_radiation = None
        self.incident_diffuse_radiation = None
        self.incident_reflected_radiation = None
        self.incident_total_radiation = None
        self.incident_total_heat_flux = None

        # Associated objects
        self._surface = surface
        self._solar_angles = solar_angles
        self._weather = weather

        # General Parameters
        self.ground_reflectance = 0.2  # Ground reflectance []
        self.absorptivity = 0.8  # Surface absorptivity []  ??? TODO Should this come from surface?

        # Add attributes from super class
        super().__init__(time)

        # Run method to update all calculated values
        self.update_calculated_values()

    def update_calculated_values(self):
        print('Updating external shortwave radiation calculations for ' + self.name)
        self.calculate_ratio_of_clear_sky_diffuse_on_horizontal_to_tilted()
        self.calculate_incident_direct_radiation()
        self.calculate_incident_diffuse_radiation()
        self.calculate_incident_reflected_radiation()
        self.calculate_incident_total_radiation()
        self.calculate_incident_total_heat_flux()

    def calculate_ratio_of_clear_sky_diffuse_on_horizontal_to_tilted(self):
        cos_incidence_angle = np.cos(np.deg2rad(self.surface.surface_solar_angles.incidence_angle))
        Y = 0.55+0.437*cos_incidence_angle+0.313*cos_incidence_angle**2
        Y[Y<0.45] = 0.45
        self.ratio_of_clear_sky_diffuse_on_horizontal_to_tilted = pd.Series(Y)

    def calculate_incident_direct_radiation(self):
        sun_on_surface = self.surface.surface_solar_angles.sun_on_surface.astype(float)
        incidence_angle = np.deg2rad(self.surface.surface_solar_angles.incidence_angle)
        direct_normal_radiation = self.weather.direct_normal_radiation
        incident_direct_radiation = direct_normal_radiation*np.cos(incidence_angle)
        incident_direct_radiation[sun_on_surface == 0] = 0.0
        incident_direct_radiation[np.cos(incidence_angle) < 0] = 0.0
        self.incident_direct_radiation = pd.Series(incident_direct_radiation)

    def calculate_incident_diffuse_radiation(self):
        incidence_angle = np.deg2rad(self.surface.surface_solar_angles.incidence_angle)
        rad_surface_tilt = np.deg2rad(self.surface.tilt)
        diffuse_horizontal_radiation = self.weather.diffuse_horizontal_radiation
        Y = self.ratio_of_clear_sky_diffuse_on_horizontal_to_tilted
        if self.surface.tilt<=90:
            incident_diffuse_radiation = diffuse_horizontal_radiation*(Y*np.sin(rad_surface_tilt)+np.cos(rad_surface_tilt))
        else:
            incident_diffuse_radiation = diffuse_horizontal_radiation*Y*np.sin(rad_surface_tilt)

        self.incident_diffuse_radiation = pd.Series(incident_diffuse_radiation)

    def calculate_incident_reflected_radiation(self):
        ground_reflectance = self.ground_reflectance
        direct_solar_radiation = self.weather.direct_normal_radiation  # TODO Check which value this should be???
        diffuse_solar_radiation = self.weather.diffuse_horizontal_radiation  # TODO Check which value this should be???
        rad_solar_altitude = np.deg2rad(self.solar_angles.solar_altitude)
        rad_surface_tilt = np.deg2rad(self.surface.tilt)
        incident_reflected_radiation = ground_reflectance*(direct_solar_radiation*np.sin(rad_solar_altitude)+diffuse_solar_radiation)*(1-np.cos(rad_surface_tilt))
        self.incident_reflected_radiation = pd.Series(incident_reflected_radiation)

    def calculate_incident_total_radiation(self):
        incident_direct_radiation = self.incident_direct_radiation
        incident_diffuse_radiation = self.incident_diffuse_radiation
        incident_reflected_radiation = self.incident_reflected_radiation
        incident_total_radiation = incident_direct_radiation + incident_diffuse_radiation + incident_reflected_radiation
        self.incident_total_radiation = pd.Series(incident_total_radiation)

    def calculate_incident_total_heat_flux(self):
        absorptivity = self.absorptivity
        incident_total_radiation = self.incident_total_radiation
        incident_total_heat_flux = absorptivity*incident_total_radiation
        self.incident_total_heat_flux = pd.Series(incident_total_heat_flux)

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

    @property
    def weather(self):
        return self._weather

    @weather.setter
    def weather(self, value):
        self._weather = value
        self.update_calculated_values()


class ExternalLongwaveRadiation:
    def __init__(self, time, surface, horizontal_infrared_radiation_sky, surface_temperature, ambient_temperature, sky_temperature):
        self.surface = surface

        # Radiation parameters
        self.sigma = 5.67e-8  # stephan-boltzmann constant
        self.absorptivity = 0.90

        # Weather data
        self.horizontal_infrared_radiation_sky = horizontal_infrared_radiation_sky

        # Temperatures
        self.surface_temperature = surface_temperature  # surface temperature [C]
        self.ambient_temperature = ambient_temperature  # ambient temperature [C]
        self.sky_temperature = self.calculate_sky_temperature()  # sky temperature [C]

        # View factors
        self.ground_view_factor = self.calculate_ground_view_factor()
        self.sky_view_factor = self.calculate_sky_view_factor()
        self.air_view_factor = self.calculate_air_view_factor()

        # Heat transfer components
        self.ground_radiative_heat_transfer = self.calculate_ground_long_wave_radiation()
        self.sky_radiative_heat_transfer = self.calculate_sky_long_wave_radiation()
        self.air_radiative_heat_transfer = self.calculate_air_long_wave_radiation()
        self.total_radiative_heat_transfer = self.calculate_total_long_wave_radiation()

        # Add attributes from super class
        super().__init__(time)

    def calculate_sky_temperature(self):
        sigma = self.sigma
        horizontal_infrared_radiation_sky = self.horizontal_infrared_radiation_sky
        sky_temp = (horizontal_infrared_radiation_sky/sigma)**0.25-273.15
        return sky_temp

    def calculate_ground_view_factor(self):
        rad_surface_tilt = np.deg2rad(self.surface_tilt)
        ground_view_factor = 0.5*(1-np.cos(rad_surface_tilt))
        return ground_view_factor

    def calculate_sky_view_factor(self):
        rad_surface_tilt = np.deg2rad(self.surface_tilt)
        sky_view_factor = 0.5*(1+np.cos(rad_surface_tilt))
        return sky_view_factor

    def calculate_air_view_factor(self):
        return 1

    def calculate_ground_long_wave_radiation(self):
        amb_temp = self.ambient_temperature
        abs_amb_temp = self.ambient_temperature+273
        surf_temp = self.surface_temperature
        abs_surf_temp = self.surface_temperature+273
        hrgnd = self.absorptivity*self.sigma*self.ground_view_factor*((abs_amb_temp)**4-(abs_surf_temp)**4)/(amb_temp-surf_temp)
        return hrgnd

    def calculate_sky_long_wave_radiation(self):
        sky_temp = self.sky_temperature
        abs_sky_temp = self.sky_temperature+273
        surf_temp = self.surface_temperature
        abs_surf_temp = self.surface_temperature+273
        hrsky = self.absorptivity*self.sigma*self.sky_view_factor*((abs_sky_temp)**4-(abs_surf_temp)**4)/(sky_temp-surf_temp)
        return hrsky

    def calculate_air_long_wave_radiation(self):
        amb_temp = self.ambient_temperature
        abs_amb_temp = self.ambient_temperature+273
        surf_temp = self.surface_temperature
        abs_surf_temp = self.surface_temperature+273
        hrair = oself.absorptivity*self.sigma*self.air_view_factor*((abs_amb_temp)**4-(abs_surf_temp)**4)/(amb_temp-surf_temp)
        return hrair

    def calculate_total_long_wave_radiation(self):
        total_radiation = self.ground_radiative_heat_transfer + self.sky_radiative_heat_transfer + self.air_radiative_heat_transfer
        return total_radiation
