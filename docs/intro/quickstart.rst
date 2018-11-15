===============
Quick Start
===============

Base Classes
============
Creating a Sitka model requires the use of several base classes.

- Settings: Contains global simulation settings
- Site: General location parameters for the building site
- Time: Construct of time index and date-time arrays used to define the time-series for the simulation.

Solar and Weather Classes
=========================
Hourly weather data can be imported from US DOE EPW weather files using the
WeatherFile class.

The SolarAngles class is used to calculate the global sun position that can be
used in shading and solar radiation calculations.
