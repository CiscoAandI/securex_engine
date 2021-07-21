import pytest
import json

from runner import Runner


class TestFoo:
    FLOW_NAME = 'definition_workflow_01P8H5A2BA6CY0wPhlr4vRoN1QpEONdaebQ'

    @pytest.mark.vcr
    def test_positive_1(self):
        runner = Runner(flow_name=TestFoo.FLOW_NAME, test_name='1')
        output = runner.run()
        assert output == runner._expected_output

    # @pytest.mark.vcr
    def test_positive_1(self):
        import requests_mock
        with requests_mock.Mocker() as m:
            agents = [{"foo": "bar"}]
            alert = {"alert": [{"agents": agents}]}
            m.get('https://api.thousandeyes.com/v6/alerts.json', json=alert)
            runner = Runner(flow_name=TestFoo.FLOW_NAME, test_name='1')
            output = runner.run()
            
            # Assert expected subset output
            assert all(item in output['definition_activity_01P8H5BY2GTCD2XRZTCnaA48vcycBrsNpJx']['output'].items() for item in {
                'variable_workflow_01PK4N9LD54DY3HRaXY47znv4QoLXcSNtnt': json.dumps(agents),
                'error': {'code': 0, 'message': 'No Error'},
                'succeeded': True,
                'variable_workflow_01PCUUR2HGW9L04MdbiDgltiMdxEeuQJKYU': json.dumps(alert),
                'variable_workflow_01PEDOYDR24CZ1BVTnT8WGN9HjVI8W8WJ8y': '[]',
                'variable_workflow_01PK3W2CU6JRF4zpXn6lvTMdicRHs6QfxZ0': '[]',
            }.items())