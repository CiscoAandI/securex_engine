import sys
import json

from actions import BaseAction

class Action(BaseAction):
    def string_cast(self, x):
        if not isinstance(x, str):
            x = json.dumps(x)
            # Need to remove "'s at the beginning and end of the json dumps if they exist.
            if x.startswith('"') and x.endswith('"'):
                return x[1:-1]
        return x

    def execute(self, script, script_queries, script_arguments=[]):
        # Mock sys.argv
        og_argv = sys.argv
        args = [self.string_cast(i) for i in script_arguments]
        sys.argv = ['FAKE_SCRIPT_NAME.py'] + args
        
        try:
            # Should use a docker container to sandbox this probably.
            exec(script)
        finally:
            og_argv = sys.argv

        # Be careful here not to overwrite script arguments
        a23dc2368_7085_483a_a77c_c1ebdb2a779e = {}

        # Parse script queries
        for script_query in script_queries:
            a23dc2368_7085_483a_a77c_c1ebdb2a779e1 = locals()[script_query['script_query']]
            if not isinstance(a23dc2368_7085_483a_a77c_c1ebdb2a779e1, bool):
                a23dc2368_7085_483a_a77c_c1ebdb2a779e1 = str(a23dc2368_7085_483a_a77c_c1ebdb2a779e1)
            a23dc2368_7085_483a_a77c_c1ebdb2a779e[script_query['script_query_name']] = a23dc2368_7085_483a_a77c_c1ebdb2a779e1

        return {'script_queries': a23dc2368_7085_483a_a77c_c1ebdb2a779e}