from actions import BaseAction
from data import OPERATOR_MAP
from core.logger import logger

class Action(BaseAction):
    def execute(self, condition, **kwargs):
        conditions = []
        
        for branch in [condition.get('left_operand'), condition.get('right_operand')]:
            if isinstance(branch, dict):
                # Recurse
                branch = self.execute(branch, **kwargs)['result']
            
            conditions.append(branch)
        
        operator = OPERATOR_MAP.get(condition.get('operator'))
        
        if not operator:
            raise NotImplementedError
        else:
            result = operator(*conditions)
            logger.info(f"Condition is {result}")
            return {
                'result': result
            }