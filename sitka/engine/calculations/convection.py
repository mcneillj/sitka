import numpy as np


class OutsideConvection:
    def __init__(self):
        self.heat_transfer_coefficient = 22.7 # Convection coefficient [W/m^2-K]
        self.wind_speed = None
        self.surface_height = None

    def calculate_coefficient(self):
        self.wind_speed = self.wind_speed*((270/10)^0.14*(0.5*self.surface_height/370)^0.22)
        # Outside convection coefficient
        D = 10.79
        E = 4.192
        F = 0.0
        self.heat_transfer_coefficient = D+E*self.wind_speed+F*self.wind_speed^2


class InsideConvection:
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
