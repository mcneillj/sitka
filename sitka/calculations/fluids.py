"""Psychrometric calculations.
"""
import numpy as np
import pandas as pd

from sitka.utils.time_series import TimeSeriesComponent


class MoistAir: #(TimeSeriesComponent):
    """Models psychrometric properties for moist air
    Parameters
    ----------
    time
    site

    Attributes
    ----------
    standard_pressure : Float
        Standard pressure [Pa].
    standard_temperature : Float
        Standard temperature [C].
    dry_air_specific_heat : Float
        Dry air specific heat [J/kg-K].
    water_vapor_specific_heat : Float
        Water vapor specific heat [J/kg-K].
    pressure : Float
        Air pressure [Pa].
    dry_bulb_temperature : Float
        Dry-bulb temperature [C].
    wet_bulb_temperature : Float
        Wet-bulb temperature [C].
    dew_point_temperature : Float
        Dew-point temperature [C].
    humidity_ratio : Float
        Humidity ratio [kg_w/kd_da].
    relative_humidity : Float
        Relative humidity [].
    moist_air_density : Float
        Moist air density [kg/m^3]
    """
    def __init__(self, time, site):
        #self.volume_flow_rate = None
        #self.mass_flow_rate = None

        # Moist air parameters
        self.pressure = None
        self.dry_bulb_temperature = None
        self.wet_bulb_temperature = None
        self.dew_point_temperature = None
        self.humidity_ratio = None
        self.relative_humidity = None
        self.moist_air_density = None

        # Moist air properties
        self.standard_pressure = None
        self.standard_temperature = None
        self.dry_air_specific_heat = 1000
        self.water_vapor_specific_heat = 1864

        # General Properties
        self._site = site

        # Add attributes from super class
        #super().__init__(time)

        # Run method to update all calculated values
        #self.update_calculated_values()

    def update_calculated_values(self):
        pass

    """
    def calculate_volume_flow_rate(self):

        volumeflowrate = zeros(len(massflowrate))
        volumeflowrate[massflowrate > 0] = massflowrate[massflowrate > 0]/density[massflowrate > 0]

        return volumeflowrate
    """

    def calculate_standard_pressure(self):
        """
        Calculate the standard pressure for a site elevation.

        Parameters
        ----------
        elevation : Float

        Yields
        ----------
        standard_pressure : Float

        References
        --------
        2009 ASHRAE Handbook of Fundamentals, Chapter 1
        """
        elevation = self.site.elevation
        standard_pressure = 101.325*(1.0-2.25577*10**-5*elevation)**5.2559
        self.standard_pressure = standard_pressure

    def set_temperature(self, temperature):
        self.temperature = pd.Series(temperature)

    def set_pressure(self, pressure):
        self.pressure = pd.Series(pressure)

    def set_humidity_ratio(self, humidity_ratio):
        self.humidity_ratio = pd.Series(humidity_ratio)

    def calculate_density(self):
        """
        Calculate the moist air density for a Series.

        Parameters
        ----------
        pressure : Series

        Yields
        ----------
        density : Series

        References
        --------
        2009 ASHRAE Handbook of Fundamentals, Chapter 1
        """

        pressure = self.pressure
        temperature = self.dry_bulb_temperature
        humidity_ratio = self.humidity_ratio
        density = 1/(0.370486 * (temperature + 459.67) * (1 + 1.607858 * humidity_ratio) / (pressure))
        self.density = pd.Series(density)


    """
    def calculate_standard_temperature(self):
        #SOURCE: 2009 ASHRAE Handbook of Fundamentals, Chapter 1
        temperature = 59 - 0.00356620*elevation
        return temperature

    def calculate_water_vapor_saturation_pressure(self):
        #Determine coefficients for IP units
        if (temperature <= 32):
            Coeff = [-1.0214165e4, -4.8932428e0, -5.3765794e-3, 1.9202377e-7, 3.5575832e-10, -9.0344688e-14 ,4.1635019e0]
        elif (temperature > 32):
            Coeff = [-1.0440397e4, -1.1294650e1, -2.7022355e-2, 1.2890360e-5, -2.4780681e-9, 0, 6.5459673e0]
        Tabs = temperature + 459.67
        #Calculate the water vapor saturation pressure [psia] from temperature [R]
        water_vapor_saturation_partial_pressure = math.exp(Coeff[0]/Tabs + Coeff[1] + Coeff[2]*Tabs + Coeff[3]*Tabs**2 + Coeff[4]*Tabs**3 + Coeff[5]*Tabs**4 + Coeff[6]*math.log(Tabs))
        return water_vapor_saturation_partial_pressure

    def calculateWaterVaporPartialPressureFromRelativeHumidity(self, relative_humidity, water_vapor_saturation_partial_pressure):
        #SOURCE:  2009 ASHRAE Handbook of Fundamentals, Chapter 1
        #Calculate water vapor partial pressure in psia
        water_vapor_partial_pressure = relative_humidity*water_vapor_saturation_partial_pressure
        return water_vapor_partial_pressure

    def calculateSaturationHumidityRatio(self, pressure, water_vapor_saturation_partial_pressure):
        #SOURCE:  2009 ASHRAE Handbook of Fundamentals, Chapter 1
        #Calculate humidity ratio of saturated air
        humidity_ratio_saturation = 0.621945 * water_vapor_saturation_partial_pressure / (pressure - water_vapor_saturation_partial_pressure)
        return humidity_ratio_saturation

    def calculateHumidityRatio(self, pressure, water_vapor_partial_pressure):
        #SOURCE:  2009 ASHRAE Handbook of Fundamentals, Chapter 1
        #Calculate the humidity ratio from pressures in psia
        humidity_ratio = 0.621945 * water_vapor_partial_pressure / (pressure - water_vapor_partial_pressure)
        #humidRat [lbw/lbda], self.water_vapor_partial_pressure [psia], p [psia]#End Function
        return humidity_ratio

    def calculateRelativeHumidity(self, pressure, water_vapor_partial_pressure, degree_of_saturation):
        #SOURCE:  2009 ASHRAE Handbook of Fundamentals, Chapter 1
        relative_humidity = min(degree_of_saturation / (1 - (1 - degree_of_saturation) * (water_vapor_partial_pressure / pressure)), 1.0)
        # relHum [], degSat [], self.water_vapor_partial_pressure [psia], p [psia]#End Function
        return relative_humidity

    def calculateDegreeOfSaturation(self, humidity_ratio, humidity_ratio_saturation):
        #SOURCE:  2009 ASHRAE Handbook of Fundamentals, Chapter 1
        degree_of_saturation = humidity_ratio/humidity_ratio_saturation
        return degree_of_saturation

    def calculateSpecificVolume(self, pressure, temperature, humidity_ratio):
        #SOURCE:  2009 ASHRAE Handbook of Fundamentals, Chapter 1
        #Label of in hg is incorrect in fundamentals.  Should be in psia
        #pHg = self.units.convertPressure(pressure,'psi','inhg')
        specific_volume = 0.370486 * (temperature + 459.67) * (1 + 1.607858 * humidity_ratio) / (pressure)
        # specVolAir [ft3/lbda], T [F], W [lbw/lbda], p [in Hg]
        return specific_volume

    def calculateMixedAirDensity(self, pressure, temperature, humidity_ratio):
        #pHg = self.units.convertPressure(pressure,'psi','inhg')
        #Label of in hg is incorrect in fundamentals.  Should be in psia


        # Check to see if value is in float or array format
        if isinstance(pressure, ndarray):
            max_pressure = max(pressure)
            max_humidity = max(humidity_ratio)
        else:
            max_pressure = pressure
            max_humidity = humidity_ratio

        # Check to see if values exist in arrays
        if max_pressure > 0 and max_humidity > 0:
            mixed_air_density = 1/(0.370486 * (temperature + 459.67) * (1 + 1.607858 * humidity_ratio) / (pressure))
            # mixAirDens [lbda/ft3], T [F], W [lbw/lbda], p [in Hg]
        else:
            mixed_air_density = zeros(len(pressure))

        return mixed_air_density

    def calculateDewPointTemperature(self, water_vapor_partial_pressure):
        #SOURCE:  2009 ASHRAE Handbook of Fundamentals, Chapter 1
        temperature_dew_point = 100.45 + 33.193*math.log(water_vapor_partial_pressure) + 2.319*math.log(water_vapor_partial_pressure)**2 + 0.17074*math.log(water_vapor_partial_pressure)**3 + 1.2063*(water_vapor_partial_pressure)**0.1984
        if (temperature_dew_point < 32):
            temperature_dew_point = 90.12 + 26.142*math.log(water_vapor_partial_pressure) + 0.8927*math.log(water_vapor_partial_pressure)**2
        return temperature_dew_point

    def calculateWetBulbTemperature(self, temperature, relative_humidity):
        #SOURCE: Stull, 2011.  "Wet-bulb temperature from relative humidity and air temperature". Journal of Applied Meteorology and Climatology.
        #applicable to temperatures between -20 and 50 C and RH between 5% and 100%
        relative_humidity = relative_humidity*100.0
        temperature = self.units.convert_units('temperature', temperature, 'F', 'C')
        temperature_wetbulb = temperature*math.atan(0.151977*(relative_humidity+8.313659)**0.5) + math.atan(temperature + relative_humidity) - math.atan(relative_humidity - 1.676331) + 0.00391838*(relative_humidity)**1.5*math.atan(0.023101*relative_humidity) - 4.686035
        temperature_wetbulb = self.units.convert_units('temperature', temperature_wetbulb, 'C', 'F')
        return temperature_wetbulb

    def calculateDryAirSpecificEnthalpy(self, temperature):
        #SOURCE:  2009 ASHRAE Handbook of Fundamentals, Chapter 1
        enthalpy = self.dry_air_specific_heat*temperature
        return enthalpy

    def calculateWaterVaporSpecificEnthalpy(self, temperature, humidity_ratio):
        #SOURCE:  2009 ASHRAE Handbook of Fundamentals, Chapter 1
        enthalpy = humidity_ratio*(1061.0+self.water_vapor_specific_heat*temperature)
        return enthalpy

    def calculateMixedAirSpecificEnthalpy(self, temperature, humidity_ratio):
        #SOURCE:  2009 ASHRAE Handbook of Fundamentals, Chapter 1
        enthalpy =self.dry_air_specific_heat*temperature + humidity_ratio*(1061.0+self.water_vapor_specific_heat*temperature)
        return enthalpy
    """

    @property
    def site(self):
        return self._site

    @site.setter
    def site(self, value):
        self._site= value
        self.update_calculated_values()
