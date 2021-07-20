import json
import pprint
import sys
import yaml

from base import Base
from workflow import Workflow
from runtime_user import RuntimeUser
from target import Target
from core.instance_validator import Validator
from core.secret_retriever import SecretRetriever
from data import GLOBALS
from exceptions import StopEngineException
from core.logger import logger


class Engine:
    def __init__(self, file_path, input={}):
        self._secret_retriever = SecretRetriever
        self._file_path = file_path
        self._spec = json.load(open(self._file_path))
        self.validate()
        
        self.populate_account_keys()
        for variable_type in ['input', 'output', 'local']:
            setattr(self, variable_type, {
                i['unique_name']: input.get(i['unique_name'], i['properties']['value'])
                for i in self._spec.get('workflow', {}).get('variables', [])
                if i['properties']['scope'] == variable_type
            })
        self.activity = {}
        # Need to name this "global" since that's what SXO calls it, however doing self.global = is a syntax error
        # for obvious python reasons.
        setattr(self, 'global', GLOBALS)
    
    def populate_account_keys(self):
        for user in self._spec.get('runtime_users', []):
            self._spec['runtime_users'][user] = self._secret_retriever.get_account_key(user)

    def validate(self):
        # Validate with json schema from workflow_spec.json
        errors = Validator(self._spec).validate()
        if errors:
            for error in errors:
                logger.error(error)
            raise errors[0]
        else:
            logger.info(f"No errors in {self._file_path}")

    @property
    def workflow(self):
        return Workflow(self, self._spec.get('workflow', {}))
    
    @property
    def variables(self):
        return self.workflow.variables

    @property
    def targets(self):
        return {k: Target(self, v) for k, v in self._spec.get('targets', {}).items()}
    
    @property
    def target(self):
        if len(self.targets) == 1:
            return [i for i in self.targets.values()][0]
        else:
            # More than one target is specified, this workflow does not have a singular target
            raise NotImplementedError

    @property
    def runtime_users(self):
        return {k: RuntimeUser(self, v) for k, v in self._spec.get('runtime_users', {}).items()}

    def run(self):
        try:
            return self.workflow.run()
        except StopEngineException as e:
            print(e)
            return self.activity


if __name__ == "__main__":
    import os
    
    _input = json.load(open(sys.argv[2])) if len(sys.argv) > 2 else {}
    engine = Engine(file_path=sys.argv[1], input=_input)
    engine.run()
    json.dump({
        'activity': engine.activity,
        'output': engine.output
    }, open('log.json', 'w'), default=dict, indent=4, sort_keys=False)