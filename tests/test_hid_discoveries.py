import pytest

def test_discover_devices(hid_fixture):
    devices = hid_fixture.enumerate()
    assert len(devices) >0