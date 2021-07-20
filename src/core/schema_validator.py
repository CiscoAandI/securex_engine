import json
from core.logger import logger

SCHEMA = "src/core/workflow_spec.json"

class Validator:
    cache = []
    
    def __init__(self, spec):
        self._spec = spec
    
    def validate(self):
        self.resolve_spec()
        tested = set([i.replace('#/definitions/', '') for i in self.cache])
        actual = set(self._spec['definitions'].keys())
        assert tested == actual, f"There are superfluous definitions. Please remove: {actual.difference(tested)}"
    
    def resolve_spec(self, subspec=None):
        if subspec is None:
            subspec = self._spec

        for k,v in subspec.items():
            if type(v) == dict and "$ref" in v and v['$ref'] not in self.cache:
                subspec[k] = self.resolve_ref(v['$ref'])
            elif type(v) == dict:
                self.resolve_spec(subspec[k])
    
    def resolve_ref(self, ref):
        logger.debug(ref)
        self.cache.append(ref)
        refobj = self.get_path(ref)
        self.resolve_spec(refobj)
        return refobj

    def get_path(self, ref):
        refpath = ref.split("/")[1:]
        refobj = self._spec
        for node in refpath:
            refobj = refobj[node]
        return refobj

if __name__ == "__main__":
    Validator(json.load(open(SCHEMA))).validate()