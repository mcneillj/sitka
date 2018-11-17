"""Surface used for thermal modeling of spaces.
"""
import os
import json
import numpy as np
import pandas as pd

from sitka.calculations.solar import SurfaceSolarAngles

class HeatTransferSurface:
    def __init__(self, name, time, solar_angles, weather):
        # General Properties
        self.name = name

        # Dimension properties
        self.thickness = 0
        self.height = None  # surface height [m]
        self.area = 1  # wall surface area [m^2]
        self.azimuth = None  # surface azimuth angle [deg]
        self.tilt = None  # surface tilt angle [deg]

        # Solar Properties
        self.surface_solar_angles = None
        self.external_shortwave_radiation = None

        # Associated objects
        self._solar_angles = solar_angles
        self._weather = weather

        # Add attributes from super class
        super().__init__(time)

        # Initial methods
        self.update_calculated_values()

    def update_calculated_values(self):
        if self.settings and self.time and self.solar_angles and self.weather and self.host_surface:
            self.get_host_surface_properties()
            self.setup_surface_solar_angles()
            self.setup_external_solar_radiation()
            self.setup_convection_models()

            # Setup conduction heat transfer
            self.calculate_thickness()
            self.calculate_thermal_resistance_array()
            self.calculate_thermal_capacitance_array()
            self.setup_conduction_model()

    def get_host_surface_properties(self):
        self.azimuth = self.host_surface.azimuth
        self.tilt = self.host_surface.tilt

    def setup_surface_solar_angles(self):
        self.surface_solar_angles = SurfaceSolarAngles(self.name + ' - Surface Solar Angles', self.time, self.solar_angles, self)

    def setup_external_solar_radiation(self):
        self.external_shortwave_radiation = ExternalShortwaveRadiation(self.name + ' - External Short Wave Radiation', self.time, self.solar_angles, self.weather, self)


    @property
    def settings(self):
        return self._settings

    @settings.setter
    def settings(self, value):
        self._settings = value
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
