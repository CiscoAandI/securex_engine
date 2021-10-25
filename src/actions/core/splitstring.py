import time

from actions import BaseAction
from core.logger import logger

class Action(BaseAction):
    def execute(self, input_string, boundaries):
        logger.info(f"Splitting {input_string} for {boundaries}")
        
        delimeters = [i['boundary'] for i in boundaries]
        result = []
        
        for character in input_string:
            if character in delimeters:
                result.append(input_string.split(character, 1))
                
        logger.info(f"Result is {result}")
        
        return {"parts": result}