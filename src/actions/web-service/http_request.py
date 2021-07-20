import requests
from actions import BaseAction

class Action(BaseAction):
    def execute(self, target, runtime_user, relative_url, **kwargs):
        # Only basic auth is supported right now
        if runtime_user.auth_option != "Basic":
            raise NotImplementedError

        # This makes URIs invalid. Ex: /alerts//.json -> /alerts.json
        uri = relative_url.replace('//', '/').replace('/.', '.')
        response = requests.request(
            url=f"{target.fqdn}{uri}",
            method=kwargs['method'],
            auth=(runtime_user.basic_username, runtime_user.basic_password),
            headers={
                **({'Content-Type': kwargs.get('content_type')} if kwargs.get('content_type') else {})
            },
            allow_redirects=kwargs.get('allow_auto_redirect', True)
        )

        if not kwargs.get('continue_on_error_status_code', False) and not response.ok:
            response.raise_for_status()

        # Why does SXO do an array for cookies and response headers?? This seems dumb.
        return {
            'response_body': response.text,
            'cookie': [i for i in response.cookies],
            'response_headers': [{'name': k, 'value': v} for k, v in response.headers.items()],
            'status_code': response.status_code,
            'status_text': response.reason,
        }