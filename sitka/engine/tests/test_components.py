import os
import pytest

from sitka.engine.settings import Settings
from sitka.engine.time import Time
from sitka.engine.weather import WeatherFile


def test_settings_init():
    settings = Settings('/path/to/working_directory')

    assert settings is not None
    assert settings.working_directory == '/path/to/working_directory'

def test_time_init():
    time = Time(start_hour=1, end_hour=2, time_steps_per_hour=3)

    assert time is not None
    assert time.start_hour == 1
    assert time.end_hour == 2
    assert time.time_steps_per_hour == 3
