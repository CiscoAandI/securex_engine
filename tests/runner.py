import os
import json

from engine import Engine

class Runner():
    def __init__(self, flow_name, test_name):
        input_path = f'tests/inputs/{flow_name}/{test_name}.json'
        input_data = json.load(open(input_path)) if os.path.exists(input_path) else {}
        
        self._engine = Engine(
            file_path=f'objects/automation/workflows/{flow_name}.json',
            secret_key=os.environ['SXO_LOCAL_SECRET_KEY'],
            input=input_data
        )
        self._expected_output = json.load(open(f'tests/output/{flow_name}/{test_name}.json'))
    
    def run(self):
        # Test
        self._engine.run()
        return json.loads(json.dumps(self._engine.activity, default=dict))