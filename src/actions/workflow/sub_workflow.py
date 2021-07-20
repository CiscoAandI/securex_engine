from . import subengine
from actions import BaseAction

class Action(BaseAction):
    def execute(self, **kwargs):
        return subengine(self._engine, self.unique_name, self.workflow_id, atomic=False, **kwargs)
