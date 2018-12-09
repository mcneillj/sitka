import pytest

from sitka.io.time import Time
from sitka.calculations.solar import SolarAngles, SurfaceSolarAngles
from sitka.components.site import Site
from sitka.components.surface import Surface

def test_surface_solar_angles_init():
    site = Site()
    time = Time()
    solar_angles = SolarAngles(time=time, site=site)
    surface = Surface('surface1', azimuth=0, tilt=90, width=1, height=1)
    surface_solar_angles = SurfaceSolarAngles(time, solar_angles, surface)

    assert surface_solar_angles is not None

def test_sun_surface_azimuth():
    site = Site(latitude=47.68, longitude=-122.25, elevation=20.0)
    time = Time()
    solar_angles = SolarAngles(time=time, site=site)
    surface = Surface('surface1', azimuth=0, tilt=90, width=1, height=1)
    surface_solar_angles = SurfaceSolarAngles(time, solar_angles, surface)

    assert round(surface_solar_angles.sun_surface_azimuth.max(),0) == 90.0
    assert round(surface_solar_angles.sun_surface_azimuth.min(),0) == 0.0
