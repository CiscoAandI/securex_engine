import os
import json

from engine import Engine

class Runner():
    def __init__(self, flow_name, test_name):
        input_path = f'./cassettes/{flow_name}/{test_name}.json'
        input_data = json.load(open(input_path)) if os.path.exists(input_path) else {}
        
        self._engine = Engine(
            file_path=f'./workflows/{flow_name}.json',
            input=input_data
        )
        self._expected_output = json.load(open(f'./cassettes/{flow_name}/{test_name}.json'))
    
    def run(self):
        # Test
        self._engine.run()
        return json.loads(json.dumps(self._engine.activity, default=dict))