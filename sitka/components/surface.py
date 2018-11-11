import os
import json
import numpy as np
import pandas as pd

from sitka.engine.calculations.solar_geometry import SurfaceSolarAngles
from sitka.engine.calculations.convection import InsideConvection, OutsideConvection
from sitka.engine.calculations.radiation import ExternalShortwaveRadiation
from sitka.engine.calculations.conduction import FiniteDifferenceMethod1D


def interpolate_incidence_angles(incidence_angle, **kwargs):
    angle_correction_factors = kwargs['angle_correction_factors']
    normal_shgc = kwargs['normal_shgc']

    if incidence_angle <= 40:
        angle_correction_factor = angle_correction_factors['40']
    elif (incidence_angle > 40) & (incidence_angle <= 50):
        angle_correction_factor = np.interp(incidence_angle, [40, 50], [angle_correction_factors['40'], angle_correction_factors['50']])
    elif (incidence_angle > 50) & (incidence_angle <= 60):
        angle_correction_factor = np.interp(incidence_angle, [50, 60], [angle_correction_factors['50'], angle_correction_factors['60']])
    elif (incidence_angle > 60) & (incidence_angle <= 70):
        angle_correction_factor = np.interp(incidence_angle, [60, 70], [angle_correction_factors['60'], angle_correction_factors['70']])
    elif (incidence_angle > 70) & (incidence_angle < 80):
        angle_correction_factor = np.interp(incidence_angle, [70, 80], [angle_correction_factors['70'], angle_correction_factors['80']])
    elif incidence_angle >= 80:
        angle_correction_factor = angle_correction_factors['80']
    else:
        angle_correction_factor = None

    angular_shgc = angle_correction_factor*normal_shgc

    return angular_shgc


class ConstructionLayer:
    def __init__(self):
        self.name = "concrete"
        self.density = 2240      #density [kg/m^3]
        self.specific_heat = 900        #Specific heat [J/kg-K]
        self.thickness = 2/12  #0.1524      #Wall thickness [m]
        self.thermal_conductivity = 0.0406        #U-factor [W/m^2-K]
        self.n = 1            #Finite difference nodes
        self.dx = self.thickness/self.n  # delta length [m]
        self.thermal_capacitance = self.density*self.specific_heat*self.dx  # Thermal capacitance [W/m^2-k]
        self.thermal_resistance= self.density*self.specific_heat*self.dx  # Thermal capacitance [W/m^2-k]


class Wall:
    def __init__(self, name, settings, time, solar_angles, weather, zone_air, azimuth=0, tilt=90, width=0, height=0):
        self.name = name

        # Dimension properties
        self.thickness = 0
        self.width = width
        self.height = height  # surface height [m]
        self.area = width*height  # wall surface area [m^2]
        self.azimuth = azimuth  # surface azimuth angle [deg]
        self.tilt = tilt  # surface tilt angle [deg]

        # Submodels
        self.opaque_surface = OpaqueSurface(self.name + ' Opaque Surface', settings, time, solar_angles, weather, zone_air, self) #, self.azimuth, self.tilt)

        # Associated objects
        self._settings = settings
        self._time = time
        self._weather = weather

        # Run method to update all calculated values
        self.update_calculated_values()

    def update_calculated_values(self):
        print('Updating ' + self.name + ' complete')
        print('')

    @property
    def settings(self):
        return self._settings

    @settings.setter
    def settings(self, value):
        self._settings = value
        self.update_calculated_values()

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        self._time = value
        self.update_calculated_values()

    @property
    def weather(self):
        return self._weather

    @weather.setter
    def weather(self, value):
        self._weather = value
        self.update_calculated_values()


class HeatTransferSurface:
    def __init__(self, name, settings, time, solar_angles, weather, zone_air, host_surface):
        # General Properties
        self.name = name
        #self.settings = settings
        #self.time = time
        self.layers = [ConstructionLayer(), ConstructionLayer(), ConstructionLayer()] # Outside layer is first and inside layer is last in array

        # Dimension properties
        self.thickness = 0
        self.height = None  # surface height [m]
        self.area = 1  # wall surface area [m^2]
        self.azimuth = None  # surface azimuth angle [deg]
        self.tilt = None  # surface tilt angle [deg]

        # Conduction properties
        self.thermal_resistance_array = None
        self.thermal_capacitance_array = None
        self.conduction_model = None

        # Solar Properties
        self.surface_solar_angles = None
        self.external_shortwave_radiation = None

        # Convection Properties
        self.wind_speed = None  # wind speed [m/s]
        self.outside_convection = None
        self.inside_convection = None

        # Associated objects
        self._settings = settings
        self._time = time
        self._solar_angles = solar_angles
        self._weather = weather
        self._zone_air = zone_air
        self._host_surface = host_surface

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

    def setup_convection_models(self):
        self.outside_convection = OutsideConvection()
        self.inside_convection = InsideConvection()

    def setup_conduction_model(self):
        self.conduction_model = FiniteDifferenceMethod1D(self.time, self, self.zone_air)

    def calculate_thickness(self):
        for layer in self.layers:
            self.thickness += layer.thickness

    def calculate_thermal_resistance_array(self):
        R = []

        # Outside surface layer
        layer = self.layers[0]
        R.append(layer.dx/(2*layer.thermal_conductivity)+1/self.outside_convection.heat_transfer_coefficient)

        # Layers inside the construction material
        for i in range(0, len(self.layers)-1):
            layer1 = self.layers[i]
            layer2 = self.layers[i+1]
            Rlayer1 = layer1.dx/(2*layer1.thermal_conductivity)
            Rlayer2 = layer2.dx/(2*layer2.thermal_conductivity)
            R.append(Rlayer1 + Rlayer2)

        # Inside surface layer
        layer = self.layers[-1]
        R.append(layer.dx/(2*layer.thermal_conductivity)+1/self.inside_convection.heat_transfer_coefficient)

        # Pass on value if len greater than 0
        if len(R) > 0:
            self.thermal_resistance_array = R

    def calculate_thermal_capacitance_array(self):
        C = []
        for i, layer in enumerate(self.layers):
            C.append(layer.density*layer.specific_heat*layer.dx)

        # Pass on value if len greater than 0
        if len(C) > 0:
            self.thermal_capacitance_array = C

    @property
    def settings(self):
        return self._settings

    @settings.setter
    def settings(self, value):
        self._settings = value
        self.update_calculated_values()

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        self._time = value
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

    @property
    def zone_air(self):
        return self._zone_air

    @zone_air.setter
    def zone_air(self, value):
        self._zone_air = value
        self.update_calculated_values()

    @property
    def host_surface(self):
        return self._host_surface

    @host_surface.setter
    def host_surface(self, value):
        self._host_surface = value
        self.update_calculated_values()


class OpaqueSurface(HeatTransferSurface):
    def update_calculated_values(self):
        if self.settings and self.time and self.solar_angles and self.weather and self.host_surface:
            self.get_host_surface_properties()
            self.setup_surface_solar_angles()
            self.setup_external_solar_radiation()
            self.setup_convection_models()

#            Setup conduction heat transfer
            self.calculate_thickness()
            self.calculate_thermal_resistance_array()
            self.calculate_thermal_capacitance_array()
            self.setup_conduction_model()
