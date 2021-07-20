from base import Base
from action_map import Mapper
from action_blocks import ActionBlocks


class Action(Base):
    def __init__(self, workflow, spec):
        super().__init__(workflow, spec)
        self._category, self._function_name = spec.get('type', '').split('.')
    
    @property
    def unique_name(self):
        return self._spec.get('unique_name', '')

    @property
    def category(self):
        return self._category

    @property
    def function_name(self):
        return self._function_name

    @property
    def function(self):
        try:
            return Mapper.get(self._spec.get('type', ''))
        except ModuleNotFoundError as e:
            message = f"Type '{self._spec.get('type', '')}' is not implemented. Error in action: {self._spec['name']}"
            raise NotImplementedError(message) from e
    
    @property
    def properties(self):
        return self._spec.get('properties', {})
    
    @property
    def target(self):
        if self.properties.get('target', {}).get('use_workflow_target'):
            return self._engine.target
        elif self.properties.get('execute_on_this_target') and self.properties.get('target', {}).get('target_id'):
            return self._engine.targets.get(self.properties.get('target', {}).get('target_id'))
    
    @property
    def runtime_user(self):
        if self.target and self.properties.get('runtime_user', {}).get('target_default', False):
            return self.target.runtime_user
        elif self.target:
            raise NotImplementedError
        
        # Otherwise there is no target and thus no user is necessary
    
    @property
    def blocks(self):
        return [ActionBlocks(self._engine, i) for i in self._spec.get('blocks', [])]

    @property
    def executor(self):
        return lambda: self.function(
            engine=self._engine,
            action_spec=self._spec,
            unique_name=self.unique_name,
            **{
                k: v
                for k, v in self.properties.items()
                if k not in ('target', 'runtime_user')
            },
            **({'target': self.target} if self.target else {}),
            **({'runtime_user': self.runtime_user} if self.runtime_user else {}),
            **({'blocks': self.blocks} if self.blocks else {})
        ).result

    @property
    def is_atomic(self):
        return self._spec.get('type', '') == 'workflow.atomic_workflow'

    def run(self):
        return self.executor()