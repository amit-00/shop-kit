import pytest
from datetime import timedelta

from apps.identity.domain.utils import *
    

@pytest.mark.parametrize("interval,expected_duration", [
    ("month", timedelta(days=30)),
    ("year", timedelta(days=365)),
])
def test_get_plan_duration(interval, expected_duration):
    assert get_plan_duration(interval) == expected_duration