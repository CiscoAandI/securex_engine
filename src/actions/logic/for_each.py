from action import Action as EngineAction
from actions import BaseAction
from core.logger import logger
from group import Group


class Action(BaseAction):
    def execute(self, source_array):
        # Source array comes in as list
        for x in source_array:
            self._engine.activity[self._action.unique_name]['input']['source_array[@]'] = x
            for i in self._action._spec['actions']:
                # Just run the group as itself a subworkflow on the same engine so variable scope isn't contained
                EngineAction(self._engine, i).run()
        
        if 'source_array[@]' in self._engine.activity[self._action.unique_name]['input']:
            del self._engine.activity[self._action.unique_name]['input']['source_array[@]']