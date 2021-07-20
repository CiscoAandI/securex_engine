from engine import Engine
from actions import BaseAction
from data import ATOMIC_ACTION_PATH, SUB_WORKFLOW_PATH


def subengine(engine, unique_name, workflow_id, atomic=True, **kwargs):
    path = ATOMIC_ACTION_PATH if atomic else SUB_WORKFLOW_PATH
    subengine = Engine(f'{path}{workflow_id}.json', engine._secret_key, **kwargs)
    subengine.run()
    engine.activity = {**engine.activity, unique_name: subengine.activity}
    
    # Output should be sent out with the unique_names as keys rather than the non-unique names
    # This is so that the other calls can reference these variables using the proper SXO variable syntax
    return subengine.output
