import pytest

from sitka.components.site import Site

def test_site_init():
    site = Site(latitude=40.0, elevation=100.0)

    assert site is not None
    assert site.latitude == 40.0
    assert site.longitude == 0.0
    assert site.elevation == 100.0
