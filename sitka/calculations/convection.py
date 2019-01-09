"""Inside and outside surface convection models.
"""
import numpy as np
import pandas as pd

from sitka.utils.time_series import TimeSeriesComponent


class OutsideConvection(TimeSeriesComponent):
    v
    def __init__(self, time, weather, surface, surface_temperature):
        # Model parameters
        self.heat_transfer_coefficient = None  # Convection coefficient (default 22.7) [W/m^2-K]

        # Geometric parameters
        self.surface_height = None

        # Thermal properties
        self.wind_speed = None
        self.surface_temperature = surface_temperature
        self.heat_transfer_rate = None

        # Associated objects
        self._weather = weather
        self._surface = surface

        # Add attributes from super class
        super().__init__(time)

        # Run method to update all calculated values
        self.update_calculated_values()

    def update_calculated_values(self):
        print('Updating external longwave radiation calculations.')
        self.calculate_surface_wind_speed()
        self.calculate_heat_transfer_coefficient()
        self.calculate_heat_transfer()

    def calculate_surface_wind_speed(self):
        """
        Calculate the wind speed at the surface based on the height.

        Yields
        ----------
        wind_speed : Series

        References
        --------
        """
        self.wind_speed = self.weather.wind_speed*((270/10)^0.14*(0.5*self.surface_height/370)^0.22)

    def calculate_heat_transfer_coefficient(self):
        """
        Calculate the outside convection coefficient on the surface.

        Yields
        ----------
        heat_transfer_coefficient : Series

        References
        --------
        """
        # Outside convection coefficient
        D = 10.79
        E = 4.192
        F = 0.0
        self.heat_transfer_coefficient = D+E*self.wind_speed+F*self.wind_speed^2

    def calculate_heat_transfer(self):
        """
        Calculate the heat transfer rate for the surface.

        Yields
        ----------
        heat_transfer_rate : Series

        References
        --------
        """
        # TODO add heat transfer rate calculation
        self.heat_transfer_rate = 1


class InsideConvection(TimeSeriesComponent):
    """
    Inside convection calculation for time-series.

    Parameters
    ----------
    time : Time
    weather : Weather
    surface : Surface
    surface_temperature : Series

    Attributes
    ----------
    heat_transfer_coefficient : Series
        Convection heat transfer coefficient [W/m^2-K].
    surface_height : float
        Surface height [m].
    wind_speed : Series
        Ambient wind speed [m/s].
    surface_temperature : Series
        Surface temperature [C].
    heat_transfer_rate : Series
        Heat transfer rate [W].
    time : Time
    weather : Weather
    surface : Surface
    """
    def __init__(self):
        self.heat_transfer_coefficient = 8.29 # Convection coefficient [W/m^2-K]
        self.surface_tilt = 90
        self.air_temperature = []
        self.surface_temperature = []

    def ashrae_vertical_wall(self):
        #  ASHRAE Vertical Wall Model
        delta_temperature = self.surface_temperature - self.air_temperature
        h = 1.31*np.abs(delta_temperature)**(1/3)
        h[h < 0.1] = 0.1
        return h

    def simple_natural_convection_algorithm(self):
        # Simple Natural Convection Algorithm [Walton (1983)]
        #inside_convection_coefficient = 1.31*np.abs(delta_temperature)**(1/3)
        surface_tilt = self.surface_tilt

        if (surface_tilt == 90):
            h = 3.076
            #obj.h_in(tim) = 1.31*np.abs(delta_temperature)**(1/3)
        elif (surface_tilt  < 90) & (delta_temperature > 0):
             h = 4.040
             #obj.h_in(tim) = 9.482*np.abs(delta_temperature)**(1/3)/(7.283-np.abs(np.cos(rad_surface_tilt)))
        elif (surface_tilt  < 90) & (DT < 0):
             h = 0.948
             #obj.h_in(tim) = 1.810*np.abs(delta_temperature)**(1/3)/(1.382+np.abs(np.cos(rad_surface_tilt)))
        else:
            h = 3.076

        return h

    def calculate_coefficient(self):
        # inside surface natural convection coefficient
        inside_convection_coefficient = simple_natural_convection_algorithm()
        self.heat_transfer_coefficient = inside_convection_coefficient
