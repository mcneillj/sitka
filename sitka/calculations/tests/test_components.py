import pytest

from sitka.io.time import Time
from sitka.calculations.solar import SolarAngles
from sitka.components.site import Site

def test_solar_angles_init():
    site = Site()
    time = Time()
    solar_angles = SolarAngles(time=time, site=site)

    assert solar_angles is not None
