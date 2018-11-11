import pytest

from sitka.components.site import Site

def test_us_atlantic_standard_meridian_calculation():
    # representative city: Halifax, Nova Scotia, Canada
    site = Site(latitude=44.65, longitude=-63.58)

    assert site.local_standard_meridian == -60.0

def test_us_eastern_standard_meridian_calculation():
    # representative city: Washington DC, USA
    site = Site(latitude=38.91, longitude=-77.04)

    assert site.local_standard_meridian == -75.0

def test_us_central_standard_meridian_calculation():
    # representative city: Saint Louis, MO, USA
    site = Site(latitude=38.63, longitude=-90.20)

    assert site.local_standard_meridian == -90.0

def test_us_mountain_standard_meridian_calculation():
    # representative city: Salt Lake City, UT, USA
    site = Site(latitude=40.76, longitude=-111.89)

    assert site.local_standard_meridian == -105.0

def test_us_pacific_standard_meridian_calculation():
    # representative city: Seattle, WA, USA
    site = Site(latitude=47.68, longitude=-122.25)

    assert site.local_standard_meridian == -120.0

def test_us_alaska_standard_meridian_calculation():
    # representative city: Juneau, AK, USA
    site = Site(latitude=61.22, longitude=-149.90)

    assert site.local_standard_meridian == -135.0

def test_us_hawaii_aleutian_standard_meridian_calculation():
    # representative city: Honolulu, HI, USA
    site = Site(latitude=21.31, longitude=-157.86)

    assert site.local_standard_meridian == -150.0
