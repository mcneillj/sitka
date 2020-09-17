import pytest
import numpy as np

from sitka.general.settings import Settings
from sitka.io.time import Time
from sitka.io.weather import EPW
from sitka.calculations.solar import SolarAngles, SurfaceSolarAngles
from sitka.calculations.radiation import ExternalShortwaveRadiation
from sitka.components.site import Site
from sitka.components.surface import Surface


def test_solar_angles_setter():
    settings = Settings('')
    site = Site()
    time = Time()
    solar_angles = SolarAngles(time=time, site=site)
    weather = EPW(time)
    weather.direct_normal_radiation = np.ones(time.length)
    weather.diffuse_horizontal_radiation = np.ones(time.length)
    surface = Surface('surface1', azimuth=0, tilt=90, width=1, height=1)
    surface_solar_angles = SurfaceSolarAngles(time, solar_angles, surface)
    external_shortwave_radiation = ExternalShortwaveRadiation(time, solar_angles, weather, surface, surface_solar_angles)
    external_shortwave_radiation.solar_angles = solar_angles

    assert external_shortwave_radiation.solar_angles is not None


def test_external_shortwave_radiation_init():
    settings = Settings('')
    site = Site()
    time = Time()
    solar_angles = SolarAngles(time=time, site=site)
    weather = EPW(time)
    weather.direct_normal_radiation = np.ones(time.length)
    weather.diffuse_horizontal_radiation = np.ones(time.length)
    surface = Surface('surface1', azimuth=0, tilt=90, width=1, height=1)
    surface_solar_angles = SurfaceSolarAngles(time, solar_angles, surface)
    external_shortwave_radiation = ExternalShortwaveRadiation(time, solar_angles, weather, surface, surface_solar_angles)

    assert external_shortwave_radiation is not None

def test_incident_direct_radiation():
    settings = Settings('')
    site = Site(latitude=0, longitude=0, elevation=0.0)
    time = Time()
    weather = EPW(time)
    weather.direct_normal_radiation = np.ones(time.length)
    weather.diffuse_horizontal_radiation = np.ones(time.length)
    solar_angles = SolarAngles(time=time, site=site)
    surface = Surface('surface1', azimuth=0, tilt=90, width=1, height=1)
    surface_solar_angles = SurfaceSolarAngles(time, solar_angles, surface)
    external_shortwave_radiation = ExternalShortwaveRadiation(time, solar_angles, weather, surface, surface_solar_angles)

    assert round(external_shortwave_radiation.incident_direct_radiation.max(),2) == 0.40
    assert round(external_shortwave_radiation.incident_direct_radiation.min(),2) == 0.00


def test_incident_diffuse_radiation():
    settings = Settings('')
    site = Site(latitude=0, longitude=0, elevation=0.0)
    time = Time()
    weather = EPW(time)
    weather.direct_normal_radiation = np.ones(time.length)
    weather.diffuse_horizontal_radiation = np.ones(time.length)
    solar_angles = SolarAngles(time=time, site=site)
    surface = Surface('surface1', azimuth=0, tilt=90, width=1, height=1)
    surface_solar_angles = SurfaceSolarAngles(time, solar_angles, surface)
    external_shortwave_radiation = ExternalShortwaveRadiation(time, solar_angles, weather, surface, surface_solar_angles)

    assert round(external_shortwave_radiation.incident_diffuse_radiation.max(),2) == 1.3
    assert round(external_shortwave_radiation.incident_diffuse_radiation.min(),2) == 0.55


def test_incident_reflected_radiation():
    settings = Settings('')
    site = Site(latitude=0, longitude=0, elevation=0.0)
    time = Time()
    weather = EPW(time)
    weather.direct_normal_radiation = np.ones(time.length)
    weather.diffuse_horizontal_radiation = np.ones(time.length)
    solar_angles = SolarAngles(time=time, site=site)
    surface = Surface('surface1', azimuth=0, tilt=90, width=1, height=1)
    surface_solar_angles = SurfaceSolarAngles(time, solar_angles, surface)
    external_shortwave_radiation = ExternalShortwaveRadiation(time, solar_angles, weather, surface, surface_solar_angles)

    assert round(external_shortwave_radiation.incident_reflected_radiation.max(),2) == 0.40
    assert round(external_shortwave_radiation.incident_reflected_radiation.min(),2) == 0.20


def test_incident_total_radiation():
    settings = Settings('')
    site = Site(latitude=0, longitude=0, elevation=0.0)
    time = Time()
    weather = EPW(time)
    weather.direct_normal_radiation = np.ones(time.length)
    weather.diffuse_horizontal_radiation = np.ones(time.length)
    solar_angles = SolarAngles(time=time, site=site)
    surface = Surface('surface1', azimuth=0, tilt=90, width=1, height=1)
    surface_solar_angles = SurfaceSolarAngles(time, solar_angles, surface)
    external_shortwave_radiation = ExternalShortwaveRadiation(time, solar_angles, weather, surface, surface_solar_angles)

    assert round(external_shortwave_radiation.incident_total_radiation.max(),2) == 1.55
    assert round(external_shortwave_radiation.incident_total_radiation.min(),2) == 0.76


def test_incident_heat_flux():
    settings = Settings('')
    site = Site(latitude=0, longitude=0, elevation=0.0)
    time = Time()
    weather = EPW(time)
    weather.direct_normal_radiation = np.ones(time.length)
    weather.diffuse_horizontal_radiation = np.ones(time.length)
    solar_angles = SolarAngles(time=time, site=site)
    surface = Surface('surface1', azimuth=0, tilt=90, width=1, height=1)
    surface_solar_angles = SurfaceSolarAngles(time, solar_angles, surface)
    external_shortwave_radiation = ExternalShortwaveRadiation(time, solar_angles, weather, surface, surface_solar_angles)

    assert round(external_shortwave_radiation.incident_total_heat_flux.max(),2) == 1.24
    assert round(external_shortwave_radiation.incident_total_heat_flux.min(),2) == 0.61
