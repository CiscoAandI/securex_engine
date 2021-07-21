import pytest
import json
import gzip
from unittest import mock
from freezegun import freeze_time

RESPONSE_HEADER_WHITELIST = [
    'content-type'
]


@pytest.fixture(scope='module')
def vcr_config():
    def before_record_response(response):
        # Try to decompress
        if 'gzip' in response['headers'].get('Content-Encoding', ''):
            response['body']['string'] = gzip.decompress(response['body']['string'])
        
        try:
            response['body']['string'] = json.loads(response['body']['string'])
        except json.JSONDecodeError as e:
            pass
        
        # Only keep important headers, filter out all others
        response['headers'] = {
            k: v
            for k, v in response['headers'].items()
            # Filter out X- headers to exclude things like rate limit which can vary depending on
            # record time
            if k.lower() in RESPONSE_HEADER_WHITELIST
        }
        
        return response

    return {
        # Replace the Authorization request header with "DUMMY" in cassettes
        "filter_headers": ['Authorization', 'Accept', 'Accept-Encoding', 'Connection', 'User-Agent'],
        "serializer": "yaml",
        "before_record_response": before_record_response
    }

@pytest.fixture(autouse=True)
def _mock():
    with mock.patch('time.sleep') as mock_sleep:
        # Freeze gun does not work with boto3 for SecretManager
        with freeze_time("1990-01-02 03:04:05"):
            yield