import pytest

from runner import Runner


class TestAcmeCriticalWebsiteHealth:
    FLOW_NAME = 'definition_workflow_01PLT6C492IVT09dl7dcdzSgu8NgQBuOu1Z'

    @pytest.mark.record
    def test_positive_dont_send_to_snow(self):
        runner = Runner(flow_name=TestAcmeCriticalWebsiteHealth.FLOW_NAME, test_name='dont_send_to_snow')
        output = runner.run()
        
        # TODO: This needs to be better and not so indescriminate
        assert output == runner._expected_output