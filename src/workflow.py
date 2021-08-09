from base import Base
from action import Action
from core.logger import logger

class Workflow(Base):
    @property
    def actions(self):
        return [Action(self._engine, i) for i in self._spec.get('actions', [])]

    @property
    def unique_name(self):
        return self._spec.get('unique_name')
    
    def run(self):
        logger.info("Running workflow")
        for action in self.actions:
            logger.debug(action.run())
        logger.info("Workflow completed")
        return self._engine.activity
    
    @property
    def input(self):
        return self._engine.input
    
    @property
    def output(self):
        return self._engine.output
    
    @property
    def local(self):
        return self._engine.local
    
    @property
    def variables(self):
        return self._spec.get('variables', {})
    
    @property
    def name(self):
        return self._spec.get('name', {})
    
    @property
    def title(self):
        return self._spec.get('title', {})
    
    @property
    def properties(self):
        return self._spec.get('properties', {})
