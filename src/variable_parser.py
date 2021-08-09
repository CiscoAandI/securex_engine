import re

class Parser:
    def __init__(self, workflow, string, target=None):
        self.workflow = workflow
        self.target = target
        self._string = string
        self.path_list = []
        setattr(self, 'global', getattr(self.workflow._engine, 'global', {}))
    
    @property
    def activity(self):
        return self.workflow._engine.activity
    
    def parse(self):
        if isinstance(self._string, (list, tuple)):
            return [Parser(self.workflow, i, target=self.target).parse() for i in self._string]
        elif isinstance(self._string, dict):
            return {k: Parser(self.workflow, v, target=self.target).parse() for k, v in self._string.items()}
        elif not isinstance(self._string, str):
            return self._string
        
        # Construct replace map
        paths = re.findall('\$.*?\$', self._string)
        for path in paths:
            # convert to string for replacements if it is not the only replacement in this string
            # Otherwise, we can use the original returned type.
            # It would be better if arguments coming in to certain actions if they're lists to have them stored
            # as lists rather than JSON strings.
            if self._string != path:
                self._string = self._string.replace(path, str(self.get_path(path)))
            else:
                self._string = self.get_path(path)
        return self._string
        
    def get_path(self, path):
        return self.get_variable_by_path(path)[1]
    
    def set_path(self, value):
        variable, _ = self.get_variable_by_path(self._string)
        variable_name = self._get_path_list(self._string)[-1]
        variable[variable_name] = value
        
    def _get_path_list(self, path):
        return path.strip('$').split('.')
    
    def get_variable_by_path(self, path):
        self.path_list = self._get_path_list(path)
        
        # Target group has special parse method
        if self.path_list and self.path_list[0] == 'targetgroup':
            # First value is "targetgroup" so pop this
            self.path_list.pop(0)
            # Next is the type for the target groups. However this, for some reason, uses spaces instead of a .
            # so we need to change spaces to dots
            self.path_list[0] = self.path_list[0].replace(' ', '.')
            if self.target.type != self.path_list[0]:
                raise NotImplementedError(f"Target type mismatches parse path requirements: {path}")
            self.path_list.pop(0)
            # Next key is the word "input" which is not currently used
            self.path_list.pop(0)
            # Final key
            return None, getattr(self.target, self.path_list[0])
        
        obj = self
        
        # If first key is "workflow" peak at second key to pull the correct workflow from the "subworkflows" key
        if self.path_list[0] == "workflow" and self.workflow.unique_name != self.path_list[1]:
            for subworkflow in self.workflow._engine.subworkflows:
                if subworkflow.workflow.unique_name == self.path_list[1]:
                    self.workflow = subworkflow.workflow
                    break
            else:
                raise Exception(f"Workflow with ID '{self.path_list[1]}' not found")
        
        for path_object in self.path_list[:-1]:
            # In the event a key looks like this: targetkey[0]
            # we need to handle this operation here.
            # Check if it ends with the list syntax
            list_index = re.search('\[\d+\]$', path_object)
            if list_index:
                path_object = re.sub('\[\d+\]$', '', path_object)
                list_index = int(list_index.group()[1:-1])
                
            obj = self._get_key(obj, path_object)
            
            # If it was a list object, pop the correct index off the list here
            if list_index is not None:
                obj = obj[list_index]
        
        return obj, self._get_key(obj, self.path_list[-1])
    
    def _get_key(self, obj, key):
        # skip check for workflow name. Maybe this is a TODO: to make this clean
        if not key == self.workflow.unique_name:
            if isinstance(obj, dict):
                obj = obj.get(key)
            else:
                obj = getattr(obj, key, None)

            if obj is None:
                # Variable not found, workflow is likely invalid or there is a bug in the engine
                raise NotImplementedError(f"Failed to find key: {key} in {self.path_list}")
        return obj