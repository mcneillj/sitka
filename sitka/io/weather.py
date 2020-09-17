"""Weather files and weather data imports.
"""
import os
import csv
import numpy as np
import pandas as pd

from sitka.utils.time_series import TimeSeriesComponent


class EPW(TimeSeriesComponent):
    """
    Imports and stores an EnergyPlus weather file (EPW format).

    Parameters
    ----------
    time : Time
        The year to use in starting the date-time.
    filename : string
        Filename, including path, to EPW file.

    Attributes
    ----------
    filename
    time
    header_imported
    data_imported
    stephan_boltzmann_constant : float
        Stephan-Boltzmann constant
    sky_temperature : Series
        Sky tempereature [C]
    columns
    incident_direct_radiation : Series
    year : Series
    month : Series
    day : Series
    hour : Series
    minute : Series
    datasource : Series
    dry_bulb_temperature : Series
        ambient dry bulb temperature [C]
    dew_point_temperature : Series
        ambient dew point temperature [C]
    relative_humidity : Series
        ambient relative humidity [#]
    atmospheric_pressure : Series
        atmospheric pressure [Pa]
    extraterrestrial_horizontal_radiation : Series
        extraterrestrial horizontal radiation [Wh/m2]
    extraterrestrial_direct_radiation : Series
        extraterrestrial direct radiation [Wh/m2]
    horizontal_infrared_radiation_sky : Series
        horizontal infrared radiation intensity from sky [Wh/m2]
    global_horizontal_radiation : Series
        global horizontal radiation [Wh/m2]
    direct_normal_radiation : Series
        direct normal radiation [Wh/m2]
    diffuse_horizontal_radiation : Series
        diffuse horizontal radiation [Wh/m2]
    global_horizontal_illuminance : Series
        global horizontal illuminance [lux]
    direct_normal_illuminance : Series
        direct normal illuminance [lux]
    diffuse_horizontal_illuminance : Series
        diffuse horizontal illuminance [lux]
    zenith_luminance : Series
        zenith luminance [lux]
    wind_direction : Series
        wind direction [deg]
    wind_speed : Series
        wind speed [m/s]
    total_sky_cover : Series
        total sky cover [tenths]
    opaque_sky_cover : Series
        opaque sky cover [tenths]
    visibility : Series
        visibility [km]
    ceiling_height : Series
        ceiling height [m]
    present_weather_observation : Series
        precipitable water [mm]
    present_weather_code : Series
        aerosol optical depth [thousandths]
    precipitable_water : Series
        snow depth [cm]
    aerosol_optical_depth : Series
        aerosol optical depth [thousandths]
    snow_depth : Series
        snow depth [cm]
    days_since_snow : Series
        days since last snow occurred [days]
    albedo : Series
        albedo []
    liquid_precipitation_depth : Series
        liquid precipitation depth [mm]
    liquid_precipitation_rate : Series
        liquid precipitation rate [hour]

    Methods
    -------
    update_calculated_values
    import_epw_header
    import_epw_column_data
    calculate_sky_temperature
    resample_integrated_data
    resample_instantaneous_data

    """
    def __init__(self, time, filename=None):  #weather_file_path, weather_file_name):
        self.filename = filename  # weather_file_name    #Name of weather file
        self._time = time
        self.header_imported = False
        self.data_imported = False
        self.stefan_boltzmann_constant = 5.67e-8  # Stephan-boltzmann constant
        self.columns = [
            "year",
            "month",
            "day",
            "hour",
            "minute",
            "datasource",
            "dry_bulb_temperature",  # ambient dry bulb temperature [C]
            "dew_point_temperature",  # ambient dew point temperature [C]
            "relative_humidity",  # ambient relative humidity [#]
            "atmospheric_pressure",  # atmospheric pressure [Pa]
            "extraterrestrial_horizontal_radiation",  # extraterrestrial horizontal radiation [Wh/m2]
            "extraterrestrial_direct_radiation",  # extraterrestrial direct radiation [Wh/m2]
            "horizontal_infrared_radiation_sky",  # horizontal infrared radiation intensity from sky [Wh/m2]
            "global_horizontal_radiation",  # global horizontal radiation [Wh/m2]
            "direct_normal_radiation",  # direct normal radiation [Wh/m2]
            "diffuse_horizontal_radiation",  # diffuse horizontal radiation [Wh/m2]
            "global_horizontal_illuminance",  # global horizontal illuminance [lux]
            "direct_normal_illuminance",  # direct normal illuminance [lux]
            "diffuse_horizontal_illuminance",  # diffuse horizontal illuminance [lux]
            "zenith_luminance",  # zenith luminance [lux]
            "wind_direction",  # wind direction [deg]
            "wind_speed",  # wind speed [m/s]
            "total_sky_cover",  # total sky cover [tenths]
            "opaque_sky_cover",  # opaque sky cover [tenths]
            "visibility",  # visibility [km]
            "ceiling_height",  # ceiling height [m]
            "present_weather_observation",  # precipitable water [mm]
            "present_weather_code",  # aerosol optical depth [thousandths]
            "precipitable_water",  # snow depth [cm]
            "aerosol_optical_depth",  # aerosol optical depth [thousandths]
            "snow_depth",  # snow depth [cm]
            "days_since_snow",  # days since last snow occurred [days]
            "albedo",  # albedo []
            "liquid_precipitation_depth",  # liquid precipitation depth [mm]
            "liquid_precipitation_rate",  # liquid precipitation rate [hour]
        ]
        self.location = None
        self.state = None
        self.country = None
        self.data_type = None
        self.station_id = None
        self.latitude = None
        self.longitude = None
        self.time_zone = None
        self.elevation = None
        self.dry_bulb_temperature = None
        self.dew_point_temperature = None
        self.relative_humidity = None
        self.atmospheric_pressure = None
        self.extraterrestrial_horizontal_radiation = None
        self.extraterrestrial_direct_radiation = None
        self.horizontal_infrared_radiation_sky = None
        self.global_horizontal_radiation = None
        self.direct_normal_radiation = None
        self.diffuse_horizontal_radiation = None
        self.global_horizontal_illuminance = None
        self.direct_normal_illuminance = None
        self.diffuse_horizontal_illuminance = None
        self.zenith_luminance = None
        self.wind_direction = None
        self.wind_speed = None
        self.total_sky_cover = None
        self.opaque_sky_cover = None
        self.visibility = None
        self.ceiling_height = None
        self.aerosol_optical_depth = None
        self.albedo = None
        self.liquid_precipitation_rate = None
        self.sky_temperature = None

        # Add attributes from super class
        super().__init__(time)

        # Run method to update all calculated values
        self.update_calculated_values()

    def update_calculated_values(self):
        print(self.time)
        print(self.filename)
        if self.time and self.filename:
            # Methods to import data
            self.import_epw_header()
            self.import_epw_column_data()
            self.calculate_sky_temperature()
            self.resample_integrated_data()
            self.resample_instantaneous_data()

    def import_epw_header(self):
        """
        Import header data from the EPW file.

        Yields
        ----------
        location : string
        state : string
        country : string
        data_type : string
        station_id : string
        latitude : float
        longitude : float
        time_zone : float
        elevation : float

        References
        --------
        """
        # Import to dataframe
        temp = pd.read_csv(self.filename, skiprows=0, nrows=1,header=None)
        self.location = temp[1][0] #weather station name
        self.state = temp[2][0] #state
        self.country = temp[3][0] #country
        self.data_type = temp[4][0] #type of weather data file
        self.station_id = temp[5][0] #weather station ID
        self.latitude = float(temp[6][0]) #latitude [deg]
        self.longitude = float(temp[7][0]) #longitude [deg]
        self.time_zone = float(temp[8][0]) #time zone [hr]
        self.elevation = float(temp[9][0])  #elevation [m]

        self.header_imported = True

    def import_epw_column_data(self):
        """
        Imports the column data from an EPW file.

        Yields
        ----------
        incident_direct_radiation : Series
        year : Series
        month : Series
        day : Series
        hour : Series
        minute : Series
        datasource : Series
        dry_bulb_temperature : Series
            ambient dry bulb temperature [C]
        dew_point_temperature : Series
            ambient dew point temperature [C]
        relative_humidity : Series
            ambient relative humidity [#]
        atmospheric_pressure : Series
            atmospheric pressure [Pa]
        extraterrestrial_horizontal_radiation : Series
            extraterrestrial horizontal radiation [Wh/m2]
        extraterrestrial_direct_radiation : Series
            extraterrestrial direct radiation [Wh/m2]
        horizontal_infrared_radiation_sky : Series
            horizontal infrared radiation intensity from sky [Wh/m2]
        global_horizontal_radiation : Series
            global horizontal radiation [Wh/m2]
        direct_normal_radiation : Series
            direct normal radiation [Wh/m2]
        diffuse_horizontal_radiation : Series
            diffuse horizontal radiation [Wh/m2]
        global_horizontal_illuminance : Series
            global horizontal illuminance [lux]
        direct_normal_illuminance : Series
            direct normal illuminance [lux]
        diffuse_horizontal_illuminance : Series
            diffuse horizontal illuminance [lux]
        zenith_luminance : Series
            zenith luminance [lux]
        wind_direction : Series
            wind direction [deg]
        wind_speed : Series
            wind speed [m/s]
        total_sky_cover : Series
            total sky cover [tenths]
        opaque_sky_cover : Series
            opaque sky cover [tenths]
        visibility : Series
            visibility [km]
        ceiling_height : Series
            ceiling height [m]
        present_weather_observation : Series
            precipitable water [mm]
        present_weather_code : Series
            aerosol optical depth [thousandths]
        precipitable_water : Series
            snow depth [cm]
        aerosol_optical_depth : Series
            aerosol optical depth [thousandths]
        snow_depth : Series
            snow depth [cm]
        days_since_snow : Series
            days since last snow occurred [days]
        albedo : Series
            albedo []
        liquid_precipitation_depth : Series
            liquid precipitation depth [mm]
        liquid_precipitation_rate : Series
            liquid precipitation rate [hour]

        References
        --------
        """
        # Read EPW weather file

        # Import to dataframe
        df = pd.read_csv(self.filename, skiprows=8, names=self.columns)

        # Set time index
        time_index = pd.to_datetime({
            # 'year': data['epw']['year'],  # EPW has variable years
            'year': np.ones(8760) * self.time.year,  # Set a constant as current year
            'month': pd.Series(df['month']),
            'day': pd.Series(df['day']),
            'hour': pd.Series(df['hour'])-1,
            'minute': pd.Series(df['minute']),
        })
        df.index = time_index
        self.__setattr__('datetime_range', time_index)

        # Concatenate data set to match simulation time period
        df = df[self.time.start_hour:self.time.end_hour]

        # Add as attributes to objects
        for key in df.keys():
            self.__setattr__(key, df[key])

        self.data_imported = True
        print('file imported.')

    def calculate_sky_temperature(self):
        """
        Calculate the sky temperature for each item in the series.

        Yields
        ----------
        sky_temp : Series

        References
        --------
        """
        stefan_boltzmann_constant = self.stefan_boltzmann_constant
        horizontal_infrared_radiation_sky = self.horizontal_infrared_radiation_sky
        sky_temperature = (horizontal_infrared_radiation_sky/stefan_boltzmann_constant)**0.25-273.15
        self.sky_temperature = pd.Series(sky_temperature)

    def resample_integrated_data(self):
        """
        Resamples integrated parameters by summing over the new time period.

        Yields
        --------
        extraterrestrial_horizontal_radiation
        extraterrestrial_direct_radiation
        horizontal_infrared_radiation_sky
        global_horizontal_radiation
        direct_normal_radiation
        diffuse_horizontal_radiation
        precipitable_water
        snow_depth
        liquid_precipitation_depth
        """
        if self.data_imported:
            keys = [
                "extraterrestrial_horizontal_radiation",
                "extraterrestrial_direct_radiation",
                "horizontal_infrared_radiation_sky",
                "global_horizontal_radiation",
                "direct_normal_radiation",
                "diffuse_horizontal_radiation",
                "precipitable_water",
                "snow_depth",
                "liquid_precipitation_depth",
            ]
            
            for key in keys:
                if key in self.__dict__.keys():
                    df = self.__getattribute__(key).astype(float)
                    df = df.append(pd.Series([None], index=[(df.index[-1] + pd.Timedelta(hours=1))]))
                    df = (df.resample('%ds' % self.time.time_step).fillna(method='ffill'))/self.time.time_steps_per_hour
                    df = df.drop(df.index[-1])
                    df.index = range(0, len(df.index))  # reset the index to integers

                    self.__setattr__(key, df)

    def resample_instantaneous_data(self):
        """
        Resamples instantaneous parameters by averaging over the new time period.

        Yields
        --------
        dry_bulb_temperature
        dew_point_temperature
        relative_humidity
        atmospheric_pressure
        global_horizontal_illuminance
        direct_normal_illuminance
        diffuse_horizontal_illuminance
        zenith_luminance
        wind_direction
        wind_speed
        total_sky_cover
        opaque_sky_cover
        visibility
        ceiling_height
        aerosol_optical_depth
        albedo
        liquid_precipitation_rate
        """
        if self.data_imported:
            keys = [
                "dry_bulb_temperature",
                "dew_point_temperature",
                "relative_humidity",
                "atmospheric_pressure",
                "global_horizontal_illuminance",
                "direct_normal_illuminance",
                "diffuse_horizontal_illuminance",
                "zenith_luminance",
                "wind_direction",
                "wind_speed",
                "total_sky_cover",
                "opaque_sky_cover",
                "visibility",
                "ceiling_height",
                #"present_weather_observation",
                #"present_weather_code",
                "aerosol_optical_depth",
                #"days_since_snow",
                "albedo",
                "liquid_precipitation_rate",
                "sky_temperature",
            ]
            for key in keys:
                if key in self.__dict__.keys():
                    df = self.__getattribute__(key).astype(float)
                    df = df.append(pd.Series([None], index=[(df.index[-1] + pd.Timedelta(hours=1))]))
                    df = df.fillna(method='pad')
                    df = df.resample('%ds' % self.time.time_step).interpolate(method='linear')
                    df = df.drop(df.index[-1])
                    df.index = range(0, len(df.index))  # reset the index to integers
                    self.__setattr__(key, df)

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        self._time = value
        self.resample_integrated_data()
        self.resample_instantaneous_data()
