import json
import re

from actions import BaseAction


class Action(BaseAction):
    operator_map = {
        '=': lambda x, y: x == y,
        '==': lambda x, y: x == y,
        '>': lambda x, y: x > y,
        '>=': lambda x, y: x >= y,
        '<=': lambda x, y: x <= y,
        '<': lambda x, y: x < y
    }
    name_regex = '\w+'
    operators_regex = "|".join([i for i in operator_map])
    value_regex = '[\'"].*?["\']'
    condition_regex = f'({name_regex})\s*({operators_regex})\s*({value_regex})'
    query_regex = f'{condition_regex}(\sAND\s{condition_regex})*'

    def evaluate_condition(self, condition, environment):
        name, operator, value = condition
        # Clear out ' and "
        # Left replace
        value = value.replace('"', "", 1).replace("'", "", 1)
        # right replace
        value = value[::-1].replace('"', "", 1).replace("'", "", 1)[::-1]
        
        if name not in environment:
            raise Exception(f"Argument from query '{name}' not found in table.")
        
        return Action.operator_map[operator](environment[name], value)

    def evaluate_query(self, query, environment):
        matches = re.search(Action.query_regex, query)
        if not matches:
            raise Exception("Query syntax invalid.")

        conditions = []
        # Example result: ('CustomerName', '=', "''", " AND Key = 'SysId'", 'Key', '=', "'SysId'")
        for condition in [matches.groups()[i:i+3] for i in range(0, len(matches.groups()), 4)]:
            conditions.append(self.evaluate_condition(condition, environment))
        
        # All conditions are AND'd together
        return all(conditions)

    def execute(self, columns, input_table, number_of_rows, persist_output, sorting, where_clause):
        # https://ciscosecurity.github.io/sxo-05-security-workflows/activities/tables/select
        # https://ciscosecurity.github.io/sxo-05-security-workflows/activities/tables/where-clause
        # Examples:
        #
        # id == [$variable$]
        # username == "[$variable$]"
        # firstName == "[$variable1$]" AND lastName == "[$variable2$]"
        # timestamp > [$variable$]
        # TODO: This function is not a very good parser. Under the hood, secureX uses arango
        # a good parser for arango doesn't really exist.
        parsed_table = json.loads(input_table)
        result = []
        for row in parsed_table:
            if self.evaluate_query(where_clause, row):
                result.append(row)
    
        if result:
            return {
                'output_table': result
            }
        
        raise Exception(f"Query '{where_clause}' did not match any rows in table.")

    def export(self, columns, input_table, number_of_rows, persist_output, sorting, where_clause):
        return ""
        