import pytest
import numpy as np

from sitka.io.time import Time
from sitka.io.weather import EPW
from sitka.calculations.solar import SolarAngles
from sitka.components.site import Site
from sitka.components.surface import Surface, HeatTransferSurface


def test_surface_init():
    site = Site()
    time = Time()
    solar_angles = SolarAngles(time=time, site=site)
    surface = Surface('surface1', azimuth=0, tilt=90, width=1, height=1)

    assert surface is not None


def test_heat_transfer_surface_init():
    site = Site()
    time = Time()
    solar_angles = SolarAngles(time=time, site=site)
    weather = EPW(time)
    weather.direct_normal_radiation = np.ones(time.length)
    weather.diffuse_horizontal_radiation = np.ones(time.length)
    surface = Surface('surface1', azimuth=0, tilt=90, width=1, height=1)
    ht_surface = HeatTransferSurface('ht_surface1', time, solar_angles, weather, surface)

    assert ht_surface is not None
