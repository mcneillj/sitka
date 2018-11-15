import pytest

from sitka.io.time import Time
from sitka.calculations.solar import SolarAngles
from sitka.components.site import Site

def test_gamma():
    site = Site(latitude=47.68, longitude=-122.25, elevation=20.0)
    time = Time()
    solar_angles = SolarAngles(time=time, site=site)

    assert round(solar_angles.gamma.max(),0) == 359
    assert round(solar_angles.gamma.min(),0) == 0

def test_equation_of_time():
    site = Site(latitude=47.68, longitude=-122.25, elevation=20.0)
    time = Time()
    solar_angles = SolarAngles(time=time, site=site)

    assert round(solar_angles.equation_of_time.max(),1) == 16.4
    assert round(solar_angles.equation_of_time.min(),1) == -14.3


def test_declination():
    site = Site(latitude=47.68, longitude=-122.25, elevation=20.0)
    time = Time()
    solar_angles = SolarAngles(time=time, site=site)

    assert round(solar_angles.declination.max(),2) == 23.45
    assert round(solar_angles.declination.min(),2) == -23.45
