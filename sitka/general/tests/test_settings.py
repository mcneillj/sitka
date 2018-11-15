import os
import pytest

from sitka.general.settings import Settings


def test_settings_init():
    settings = Settings('/path/to/working_directory')

    assert settings is not None
    assert settings.working_directory == '/path/to/working_directory'
