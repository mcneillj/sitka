"""Weather files and weather data imports.
"""
import os
import csv
import numpy as np
import pandas as pd

class EPW:
    def __init__(self, settings, time, filename):  #weather_file_path, weather_file_name):
        self.filename = filename  # weather_file_name    #Name of weather file
        self._time = time
        self.data_imported = False
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

        # Methods to import data
        self.import_epw_data()
        self.resampling_data()

    def import_epw_data(self):
        print('Importing weather data.')
        self.import_epw_column_data()
        self.import_epw_header()
        self.data_imported = True

    def import_epw_header(self):
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

    def import_epw_column_data(self):
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

        print('file imported.')
        # Add as attributes to objects
        for key in df.keys():
            self.__setattr__(key, df[key])

    def resampling_data(self):
        print('Resampling weather data.')
        self.resample_integrated_data()
        self.resample_instantaneous_data()

    def resample_integrated_data(self):
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
                df = self.__getattribute__(key).astype(float)
                df = df.append(pd.Series([None], index=[(df.index[-1] + pd.Timedelta(hours=1))]))
                df = (df.resample('%ds' % self.time.time_step).fillna(method='ffill'))/self.time.time_steps_per_hour
                df = df.drop(df.index[-1])

                self.__setattr__(key, df)

    def resample_instantaneous_data(self):
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
            ]
            for key in keys:
                df = self.__getattribute__(key).astype(float)
                df = df.append(pd.Series([None], index=[(df.index[-1] + pd.Timedelta(hours=1))]))
                df = df.fillna(method='pad')
                df = df.resample('%ds' % self.time.time_step).interpolate(method='linear')
                df = df.drop(df.index[-1])
                self.__setattr__(key, df)

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        self._time = value
        self.resampling_data()
