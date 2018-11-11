import pytest

from sitka.engine.time import Time
from sitka.engine.calculations.solar_geometry import SolarAngles
from sitka.components.site import Site

def test_solar_angles_init():
    site = Site()
    time = Time()
    solar_angles = SolarAngles(time=time, site=site)

    assert solar_angles is not None
