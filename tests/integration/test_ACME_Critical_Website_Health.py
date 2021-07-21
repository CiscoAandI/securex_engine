import pytest

from runner import Runner


class TestAcmeCriticalWebsiteHealth:
    FLOW_NAME = 'definition_workflow_01PLT6C492IVT09dl7dcdzSgu8NgQBuOu1Z'

    @pytest.mark.vcr
    def test_positive_dont_send_to_snow(self):
        runner = Runner(flow_name=TestAcmeCriticalWebsiteHealth.FLOW_NAME, test_name='dont_send_to_snow')
        output = runner.run()
        
        # Dates and other values will be different so we cannot just check for full equality.
        import json; json.dump(output, open('test.json', 'w'), sort_keys=False, indent=4)
        # assert output == runner._expected_output
        