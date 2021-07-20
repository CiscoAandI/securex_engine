from actions import BaseAction
from variable_parser import Parser

class Action(BaseAction):
    def execute(self, _variables_to_update):
        output = {}
        for variable in _variables_to_update:
            value = Parser(self._engine, variable['variable_value_new']).parse()
            Parser(self._engine, variable['variable_to_update']).set_path(value)
            output[variable['variable_to_update']] = value
        return output