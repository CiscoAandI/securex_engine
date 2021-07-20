import cProfile
import pstats
import io
import os
import json
from engine import Engine

FLOW_NAME = 'definition_workflow_01PLT6C492IVT09dl7dcdzSgu8NgQBuOu1Z'

_input = json.load(open(f'tests/inputs/{FLOW_NAME}/dont_send_to_snow.json'))

with cProfile.Profile() as profile:
    engine = Engine(
        file_path=f'objects/automation/workflows/{FLOW_NAME}.json',
        input=_input
    )
    engine.run()
    stream = io.StringIO()
    ps = pstats.Stats(profile, stream=stream)
    ps.sort_stats('cumtime')
    ps.print_stats()
    with open('audit.txt', 'w+') as f:
        f.write(stream.getvalue())