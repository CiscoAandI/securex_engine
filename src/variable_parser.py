import re

class Parser:
    def __init__(self, engine, string):
        self._engine = engine
        self._string = string
        self.path_list = []
    
    def parse(self):
        if isinstance(self._string, (list, tuple)):
            return [Parser(self._engine, i).parse() for i in self._string]
        elif isinstance(self._string, dict):
            return {k: Parser(self._engine, v).parse() for k, v in self._string.items()}
        elif not isinstance(self._string, str):
            return self._string
        
        # Construct replace map
        paths = re.findall('\$.*?\$', self._string)
        for path in paths:
            # Always convert to string for replacements
            self._string = self._string.replace(path, str(self.get_path(path)))
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
        
        obj = self._engine
        
        for path_object in self.path_list[:-1]:
            obj = self._get_key(obj, path_object)
        
        return obj, self._get_key(obj, self.path_list[-1])
    
    def _get_key(self, obj, key):
        # skip check for workflow name. Maybe this is a TODO: to make this clean
        if not key == self._engine.workflow.unique_name:
            if isinstance(obj, dict):
                obj = obj.get(key)
            else:
                obj = getattr(obj, key, None)
            if obj is None:
                # Variable not found, workflow is likely invalid or there is a bug in the engine
                raise NotImplementedError(f"Failed to find key: {key} in {self.path_list}")
        return obj