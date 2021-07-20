import sys
import requests
import base64
import json

class SXO:
    BASE_URL = 'https://securex-ao.us.security.cisco.com'
    
    def __init__(self, client_id, client_password):
        self.client_id = client_id
        self.client_password = client_password
        
    def _raw_request(self, *args, **kwargs):
        result = requests.request(*args, **kwargs)
        if result.ok:
            try:
                return result.json()
            except json.decoder.JSONDecodeError:
                return result.text
        else:
            result.raise_from_status()
        
    def _request(self, **kwargs):
        # Request with credentials
        headers = kwargs.pop('headers', {})
        headers['Authorization'] = f'Bearer {self._get_jwt()}'
        return self._raw_request(url=BASE_URL + kwargs.pop('url', ''), headers=headers, **kwargs)

    def _get_jwt(self):
        headers = {
            "Content-Type": "application/x-www-form-urlencoded", 
            "Accept": "application/json", 
            "Authorization": "Basic " + base64.standard_b64encode(f'{self.client_id}:{self.client_password}'.encode()).decode()
        }

        access_token = self._raw_request(
            method='post',
            url='https://visibility.amp.cisco.com/iroh/oauth2/token',
            data="grant_type=client_credentials",
            headers=headers
        )['access_token']
        
        headers['Authorization'] = f'Bearer {access_token}'
        
        return self._raw_request(
            method='post',
            url='https://visibility.amp.cisco.com/iroh/ao/gen-jwt',
            headers=headers,
            data='{}'
        )
    
    @property
    def workflows(self):
        return self._request(method='get', uri='')
    
if __name__ == "__main__":
    client_id, client_password = sys.argv[1:]
    print(SXO(client_id, client_password)._get_jwt())