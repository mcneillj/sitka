"""Surface used for thermal modeling of spaces.
"""
import os
import json
import numpy as np
import pandas as pd

from sitka.utils.time_series import TimeSeriesComponent
from sitka.calculations.solar import SurfaceSolarAngles
from sitka.calculations.radiation import ExternalShortwaveRadiation, ExternalLongwaveRadiation


class Surface:
    """
    Properties for physical surfaces.

    Parameters
    ----------
    name : string
    azimuth : float
    tilt : float
    width : float
    height : float

    Attributes
    ----------
    name : string
        Name of the surface.
    azimuth : float
        surface azimuth angle [deg].
    tilt : float
        surface tilt angle [deg].
    width : float
        surface width [m].
    height : float
        surface height [m].
    area : float
        wall surface area [m^2].
    """
    def __init__(self, name, azimuth=0, tilt=90, width=0, height=0):
        # General Properties
        self.name = name

        # Position properties
        self.azimuth = azimuth  # surface azimuth angle [deg]
        self.tilt = tilt  # surface tilt angle [deg]

        # Dimension properties
        self.width = width  # surface width [m]
        self.height = height  # surface height [m]
        self.area = width*height  # wall surface area [m^2]


class HeatTransferSurface(TimeSeriesComponent):
    """
    Object for conducting heat transfer calculations on surface.

    Parameters
    ----------
    name : string
    time : Time
    solar_angles : SolarAngles
    weather : Weather
    surface : Surface

    Attributes
    ----------
    name : string
        Name of the surface.
    surface_solar_angles : SurfaceSolarAngles
    external_shortwave_radiation : ExternalShortwaveRadiation
    external_longwave_radiation : ExternalLongwaveRadiation
    exterior_surface_temperature : Series
    time : Time
    solar_angles : SolarAngles
    weather : Weather
    surface : Surface
    surface_solar_angles : SurfaceSolarAngles
    """
    def __init__(self, name, time, solar_angles, weather, surface):
        # General Properties
        self.name = name

        # Solar Properties
        self.surface_solar_angles = None
        self.external_shortwave_radiation = None
        self.external_longwave_radiation = None

        # Thermal Properties
        self.exterior_surface_temperature = None

        # Associated objects
        self._solar_angles = solar_angles
        self._weather = weather
        self._surface = surface

        # Add attributes from super class
        super().__init__(time)

        # Initial methods
        self.update_calculated_values()

    def update_calculated_values(self):
        if self.time and self.solar_angles and self.weather:
            self.initialize_exterior_surface_temperature()
            self.setup_surface_solar_angles()
            self.setup_external_solar_radiation()

    def initialize_exterior_surface_temperature(self):
        """
        Initialize the exterior surface temperature using the ambient dry bulb
        temperature.

        Yields
        ----------
        exterior_surface_temperature : Series

        References
        --------
        """
        if self.weather.dry_bulb_temperature is not None:
            self.exterior_surface_temperature = self.weather.dry_bulb_temperature

    def setup_surface_solar_angles(self):
        """
        Create an object for surface solar angles.

        Yields
        ----------
        surface_solar_angles : SurfaceSolarAngles

        References
        --------
        """
        self.surface_solar_angles = SurfaceSolarAngles(self.time, self.solar_angles, self.surface)

    def setup_external_solar_radiation(self):
        """
        Create object for external shortwave radiation calculations.

        Yields
        ----------
        external_shortwave_radiation : ExternalShortwaveRadiation
        external_longwave_radiation : ExternalLongwaveRadiation

        References
        --------
        """
        self.external_shortwave_radiation = ExternalShortwaveRadiation(self.time, self.solar_angles, self.weather, self.surface, self.surface_solar_angles)
        self.external_longwave_radiation = ExternalLongwaveRadiation(self.time, self.weather, self.surface, self.exterior_surface_temperature)

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
        self._surface = value
        self.update_calculated_values()
