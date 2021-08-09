import json

from jsonpath_ng import jsonpath, parse
from actions import BaseAction

# Results from a standard run (without memoization)
#  3    0.001    0.000    5.396    1.799 /engine/src/actions/corejava/jsonpathquery.py:7(execute)
# 21    0.000    0.000    5.380    0.256 /usr/local/lib/python3.9/site-packages/jsonpath_ng/parser.py:13(parse)
# 21    0.001    0.000    5.379    0.256 /usr/local/lib/python3.9/site-packages/jsonpath_ng/parser.py:30(parse)
# 21    0.003    0.000    5.379    0.256 /usr/local/lib/python3.9/site-packages/jsonpath_ng/parser.py:34(parse_token_stream)
# 21    0.011    0.001    4.928    0.235 /usr/local/lib/python3.9/site-packages/ply/yacc.py:3216(yacc)
# 21    0.001    0.000    4.203    0.200 /usr/local/lib/python3.9/site-packages/ply/yacc.py:2102(__init__)
# 21    0.489    0.023    3.842    0.183 /usr/local/lib/python3.9/site-packages/ply/yacc.py:2534(lr_parse_table)
# 20664    0.714    0.000    1.757    0.000 /usr/local/lib/python3.9/site-packages/ply/yacc.py:2165(lr0_goto)

# Memoize
class Action(BaseAction):
    def string_cast(self, x):
        x = json.dumps(x)
        # Need to remove "'s at the beginning and end of the json dumps if they exist.
        if x.startswith('"') and x.endswith('"'):
            return x[1:-1]
        return x
    def execute(self, input_json, jsonpath_queries):
        result = {}
        input_json = json.loads(input_json)
        for path in jsonpath_queries:
            matches = self._get_matches(input_json, path['jsonpath_query'])
            # This leads to the annoying SXO bug where the first value is popped from the list
            if isinstance(matches, (list, tuple)) and len(matches) == 1:
                # We used to do this, but SXO always json dumps here, even if it's a string already
                # So we must imitate this bug. lmao.
                # output = json.dumps(matches[0]) if isinstance(matches[0], (list, dict, tuple)) else matches[0]
                output = self.string_cast(matches[0])
            elif isinstance(matches, dict):
                output = json.dumps(matches)
            elif isinstance(matches, (int, bool)):
                output = matches
            else:
                output = str(matches)
                
            result[path['jsonpath_query_name']] = output
        return {
            'jsonpath_queries': result
        }

    def _get_matches(self, input_json, path):
        return [match.value for match in parse(path).find(input_json)]
        