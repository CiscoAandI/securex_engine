from base import Base
from action_map import Mapper
from action_blocks import ActionBlocks

# TODO: move to data file or something
DEPTH_LIMIT = 1000

class Action(Base):
    def __init__(self, engine, spec):
        super().__init__(engine, spec)
        self._category, self._function_name = spec.get('type', '').split('.')
    
    @property
    def unique_name(self):
        return self._spec.get('unique_name', '')
    
    @property
    def workflow_id(self):
        return self.properties.get('workflow_id', '')

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
        # TODO: handle when a target group is configured against many targets.
        if self.properties.get('target', {}).get('use_workflow_target'):
            return [i for i in self._engine.targets.values()][0]
        elif self.properties.get('execute_on_this_target') and self.properties.get('target', {}).get('target_id'):
            return self._engine.targets.get(self.properties.get('target', {}).get('target_id'))
        elif self.properties.get('target', {}).get('use_workflow_target_group'):
            # TODO: handle many targets
            spec = self._engine.workflow.properties['target']['target_group']
            target_group = self._engine.target_groups[spec['target_group_id']]
            resolved = target_group.resolve_targets(self._engine.workflow, spec)
            if len(resolved) != 1:
                raise NotImplementedError("Does not support a target group that has multiple resolved targets")
            else:
                return resolved[0]
        elif self.properties.get('target', {}).get('execute_on_this_target_group') and self.properties.get('target', {}).get('target_group_id'):
            target_group = self._engine.target_groups.get(self.properties.get('target', {}).get('target_group_id'))
            if not target_group:
                # NOTE: I think this happens when the target is coded into the atomic action and is *visible* to
                # the parent workflow, but is not changable. Thus, not finding the target group is okay since
                # we will re-assess as the atomic action begins executing.
                # TODO: logger info; color coded
                print(f"INFO: target group '{self.properties.get('target', {}).get('target_group_id')}' not found")
                return
            
            # First try to get target group from top-level
            if self._engine.workflow.properties.get('target', {}).get('target_group', {}).get('target_group_id') == target_group.unique_name:
                return target_group.resolve_targets(self._engine.workflow, self._engine.workflow.properties['target']['target_group'])[0]
            
            # Next, try to get target from subworkflow
            subworkflow = [i for i in self._engine.subworkflows if i.workflow.unique_name == self.workflow_id]
            spec = subworkflow[0].workflow.properties['target']['target_group']
            return target_group.resolve_targets(subworkflow[0].workflow, spec)[0]
    
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
            action=self,
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