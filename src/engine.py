import json
import pprint
import sys
import yaml

from base import Base
from workflow import Workflow
from runtime_user import RuntimeUser
from target import Target
from target_group import TargetGroup
from core.instance_validator import Validator
from data import GLOBALS, ACCOUNT_KEYS
from exceptions import StopEngineException
from core.logger import logger


class Engine:
    def __init__(self, spec, input={}, is_subworkflow=False):
        self.is_subworkflow = is_subworkflow

        self._spec = spec
        if not is_subworkflow:
            self.validate()
        
        self.populate_account_keys()
            
        self.local = {}
        self.output = {}
        self.input = {}
        
        # Check for required inputs
        if not is_subworkflow:
            for variable in self._spec.get('workflow', {}).get('variables', []):
                if variable['properties']['scope'] == 'input' and \
                        not input.get(variable['unique_name'], variable['properties']['value']) and \
                        variable['properties']['is_required']:
                    raise Exception(f"Input Argument '{variable['properties']['name']}' is required but not provided!")
                    
        # TODO: Clean this up
        for variable_type in ['input', 'output', 'local']:
            for i in self._spec.get('workflow', {}).get('variables', []):
                setattr(self, variable_type, {
                    **getattr(self, variable_type, {}),
                    i['unique_name']: input.get(i['unique_name'], i['properties']['value'])
                })

        self.activity = {}
        # Need to name this "global" since that's what SXO calls it, however doing self.global = is a syntax error
        # for obvious python reasons.
        setattr(self, 'global', GLOBALS)
    
    def populate_account_keys(self):
        for user in self._spec.get('runtime_users', []):
            self._spec['runtime_users'][user] = ACCOUNT_KEYS[user]

    def validate(self):
        # Validate with json schema from workflow_spec.json
        errors = Validator(self._spec).validate()
        if errors:
            for error in errors:
                logger.error(error)
            raise errors[0]
        else:
            logger.info(f"No errors in spec")

    @property
    def workflow(self):
        return Workflow(self, self._spec.get('workflow', {}))

    @property
    def subworkflows(self):
        return [Engine(
            i,
            # account_keys=self._spec['runtime_users'][user]
            is_subworkflow=True,
        ) for i in self._spec.get('subworkflows', {})]
    
    @property
    def variables(self):
        return self.workflow.variables

    @property
    def targets(self):
        return {k: Target(self, v) for k, v in self._spec.get('targets', {}).items()}

    @property
    def target_groups(self):
        return {k: TargetGroup(self, v) for k, v in self._spec.get('target_groups', {}).items()}

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
    import argparse
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument('workflow', type=str, help='The workflow to execute.')
    parser.add_argument('-i', '--input', type=str, help='The path to a previously recorded VCR cassette.')
    
    args = parser.parse_args()
    
    engine = Engine(
        spec=json.load(open(args.workflow)),
        input=json.load(open(args.input)),
    )
    engine.run()
    json.dump({
        'activity': engine.activity,
        'output': engine.output
    }, open('SXO/log.json', 'w'), default=dict, indent=4, sort_keys=False)