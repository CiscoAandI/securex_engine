from actions import BaseAction
from group import Group
from core.logger import logger

class Action(BaseAction):
    def execute(self, **kwargs):
        logger.info(f"Group: {self.display_name}")
        # Just run the group as itself a subworkflow on the same engine so variable scope isn't contained
        Group(self._engine, self._action._spec).run()
