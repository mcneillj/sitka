import pytest
import numpy as np
import pandas as pd

from sitka.io.time import Time
from sitka.io.weather import EPW


def test_weather_init():
    time = Time()
    weather = EPW(time)

    assert weather is not None


def test_length_direct_normal_radiation():
    time = Time()
    weather = EPW(time)
    weather.direct_normal_radiation = pd.Series(np.ones(time.length))

    assert len(weather.direct_normal_radiation) == 35040


def test_resample_direct_normal_radiation():
    time = Time(time_steps_per_hour=2)
    weather = EPW(time)
    weather.direct_normal_radiation = pd.Series(np.ones(time.length))

    assert sum(weather.direct_normal_radiation) == 8760*2


def test_resample_dry_bulb_temperature():
    time = Time(time_steps_per_hour=1)
    weather = EPW(time)
    weather.dry_bulb_temperature = pd.Series(np.ones(time.length))

    assert sum(weather.dry_bulb_temperature) == 8760
