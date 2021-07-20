import sys
from actions import BaseAction

class Action(BaseAction):
    def execute(self, script, script_arguments, script_queries):
        # Mock sys.argv
        og_argv = sys.argv
        sys.argv = ['FAKE_SCRIPT_NAME.py'] + script_arguments
        
        try:
            # Should use a docker container to sandbox this probably.
            exec(script)
        finally:
            og_argv = sys.argv
        
        output = {}
        
        # Parse script queries
        for script_query in script_queries:
            output[script_query['script_query_name']] = str(locals()[script_query['script_query']])

        return {'script_queries': output}