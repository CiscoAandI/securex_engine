import json

from data import CAST_MAP
from jsonpath_ng import jsonpath, parse
from actions import BaseAction

class Action(BaseAction):
    def _cast(self, value, value_type): 
        if value_type not in CAST_MAP:
            raise NotImplementedError(f"Unsupported cast type: {value_type}. Please add this to the cast map.")
        
        return CAST_MAP[value_type](value)
    
    def execute(self, input_json, jsonpath_query, persist_output, populate_columns, table_columns):
        # Populate_columns -> use JSON arguments to populate table columns
        # persist_output -> returns output variable of array of dictionaries.
        matches = [match.value for match in parse(jsonpath_query).find(json.loads(input_json))]
        
        # These are not identical errors from SXO
        # TODO: Update this to match SXO errors.
        if len(matches) > 1:
            raise Exception(f"JSONPath '{jsonpath_query}' matches more than once in the input.")
        elif len(matches) == 0:
            raise Exception(f"JSONPath '{jsonpath_query}' does not match the input.")
        elif not isinstance(matches[0], (list, tuple)):
            raise Exception(f"Resulting jsonpath match for '{jsonpath_query}' is not a valid JSON array.")
        else:
            if populate_columns:
                return_value = []
                for i, row in enumerate(matches[0]):
                    # TODO: see if SXO will do a merge of columns or will require columns from the first value only
                    # For now, my assumption is it will require the same structure as the first encountered row.
                    if i != 0 and not all([i in return_value[0] for i in row.keys()]):
                        raise Exception("Keys in resulting json do not all match")
                    return_value.append(row)
                return_value = return_value
            else:
                return_value = []
                for row in matches[0]:
                    cur_row = {}
                    for column in table_columns:
                        # If a column does not exist in the input json. simply skip it
                        if column['column_name'] in row:
                            cur_row[column['column_name']] = self._cast(row[column['column_name']], column['column_type'])
                    return_value.append(cur_row)
                        
            if persist_output:
                return {'read_table_from_json': return_value}
        