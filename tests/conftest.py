import pytest
from unittest import mock
from freezegun import freeze_time

pytest.mark.record = pytest.mark.vcr(serializer='yaml', filter_headers=['Authorization'])

@pytest.fixture(autouse=True)
def _mock():
    with mock.patch('time.sleep') as mock_sleep:
        with freeze_time("1990-01-02 03:04:05"):
            yield