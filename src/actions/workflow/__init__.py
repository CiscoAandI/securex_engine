import json
import os

from engine import Engine
from actions import BaseAction
from data import ATOMIC_ACTION_PATH, SUB_WORKFLOW_PATH


def resolve_path(path, file):
    for location, folders, files in os.walk(path):
        for f in files:
            if f == file:
                return os.path.join(location, file)
    else:
        raise FileNotFoundError(f"The target file '{file}' was not found in '{path}'")


def subengine(engine, unique_name, workflow_id, atomic=True, **kwargs):
    if atomic:
        spec = json.load(open(resolve_path(ATOMIC_ACTION_PATH, workflow_id + '.json')))
    else:
        # Subworkflows inside the workflow should be ignored because importing the top-level workflow
        # before the subworkflow will *NOT* update any of the subworkflows. Instead they will just be marked as invalid
        # thus we should pull the workflow from the workflow path which is committed independently to git.
        spec = json.load(open(resolve_path(SUB_WORKFLOW_PATH, workflow_id + '.json')))
        # spec = [i for i in engine.subworkflows if i.workflow.unique_name == workflow_id][0]._spec
        
    # i'm not sure what to do with these so remove them for now.
    # TODO: maybe try to pass them in and use them?? haven't encountered a need to do that yet.
    # There should be a need when a workflow is encountered that has "specify target on workflow start" set to true
    kwargs.pop('target', None)
    kwargs.pop('runtime_user', None)
    subengine = Engine(
        spec,
        is_subworkflow=True,
        **kwargs
    )
    # Pass targets, runtime_users, and target groups down as they are contained at the top level but not always 
    # contained in subworkflows. Thus, when referenced in subworkflows they need to be available in the 
    # subworkflow engine/
    for key in ['target_groups', 'targets', 'runtime_users']:
        subengine._spec[key] = {
            **engine._spec.get(key, {}),
            **subengine._spec.get(key, {})
        }
    # Run the subengine
    subengine.run()
    engine.activity = {**engine.activity, unique_name: subengine.activity}
    
    # Output should be sent out with the unique_names as keys rather than the non-unique names
    # This is so that the other calls can reference these variables using the proper SXO variable syntax
    return subengine.output
