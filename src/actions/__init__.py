import inspect
import pprint
import traceback
import datetime

from variable_parser import Parser
from data import GLOBAL_TIMEOUT
from core.logger import logger

class BaseAction:
    def __init__(
        self, 
        engine,
        action,
        unique_name,
        continue_on_failure=False,
        display_name="Default Display",
        skip_execution=False,
        description="Default Description",
        workflow_id='',
        action_timeout=GLOBAL_TIMEOUT,
        **kwargs
    ):
        self._engine = engine
        self._action = action
        self.continue_on_failure = continue_on_failure
        self.display_name = display_name
        self.skip_execution = skip_execution
        self.description = description
        self.workflow_id = workflow_id
        self.action_timeout = action_timeout
        self.unique_name = unique_name
        self.result = self._executor(self.execute, **kwargs)
    
    def _executor(self, f, **kwargs):
        logger.debug(f"Continue On Failure: {self.continue_on_failure}")
        logger.info(f"Display Name: {self.display_name}")
        logger.debug(f"Skip Execution: {self.skip_execution}")
        logger.debug(f"Description: {self.description}")
        logger.debug(f"Workflow ID: {self.workflow_id}")
        logger.debug(f"Action Timeout: {self.action_timeout}")
        logger.info(f"Unique Name: {self.unique_name}")
        
        new_kwargs = {}
        for k, v in kwargs.items():
            # If underscore arg is provided, don't mutate args
            if f'_{k}' in inspect.getargs(f.__code__)._asdict().get('args', []):
                new_kwargs[f"_{k}"] = v
            else:
                new_kwargs[k] = Parser(self._engine.workflow, v).parse()
        logger.debug(f"Kwargs: {pprint.pformat(new_kwargs)}")

        if not self.skip_execution:
            try:
                # Set the key here so the order shows up correctly in the logs
                # This way, this activity will appear *before* its children
                self._engine.activity[self.unique_name] = {}
                variable_map = {}
                variable_map['name'] = self.display_name
                variable_map['input'] = new_kwargs
                
                # Save because some atomics need access to the input (for_each)
                self._engine.activity[self.unique_name] = variable_map
                
                start_time = datetime.datetime.utcnow()
                variable_map['output'] = f(**new_kwargs) or {}
                end_time = datetime.datetime.utcnow()
                variable_map['elapsed_time'] = str(end_time - start_time)
                variable_map['start_time'] = start_time.isoformat()
                variable_map['end_time'] = end_time.isoformat()
                variable_map['error'] = {
                    'code': 0,
                    'message': 'No Error'
                }
                self._engine.activity[self.unique_name] = variable_map
                return variable_map
            except Exception as e:
                if not self.continue_on_failure:
                    raise
                else:
                    logger.error(traceback.format_exc())
                    logger.info("Continuing after failure.")
