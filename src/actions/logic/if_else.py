from action import Action as EngineAction
from group import Group
from actions import BaseAction
from core.logger import logger

class Action(BaseAction):
    def execute(self, blocks, **kwargs):
        # For each condition, check and execute sub workflow
        for subworkflow in blocks:
            # If condition is true, run subworkflow
            result = EngineAction(self._engine, subworkflow._spec).run().get('output', {}).get('result', False)
            if result:
                # If a condition is executed, do not check additional conditions
                Group(self._engine, subworkflow._spec).run()
                break
            else:
                logger.info("Not executing action")