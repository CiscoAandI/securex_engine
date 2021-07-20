from actions import BaseAction
from engine import Workflow
from core.logger import logger

class Action(BaseAction):
    def execute(self, **kwargs):
        logger.info(f"Group: {self.display_name}")
        # Just run the group as itself a subworkflow on the same engine so variable scope isn't contained
        Workflow(self._engine, self._action_spec).run()
