import os
import pytest

from sitka.io.time import Time

def test_time_init():
    time = Time(start_hour=1, end_hour=2, time_steps_per_hour=3)

    assert time is not None
    assert time.start_hour == 1
    assert time.end_hour == 2
    assert time.time_steps_per_hour == 3
