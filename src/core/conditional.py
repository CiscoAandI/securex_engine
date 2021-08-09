from data import OPERATOR_MAP
from core.logger import logger

def evaluate_conditional(condition):
    conditions = []
    
    for branch in [condition.get('left_operand'), condition.get('right_operand')]:
        if isinstance(branch, dict):
            # Recurse
            branch = evaluate_conditional(branch)['result']
        
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