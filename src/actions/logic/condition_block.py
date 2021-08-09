from actions import BaseAction
from core.conditional import evaluate_conditional

class Action(BaseAction):
    def execute(self, condition):
        return evaluate_conditional(condition)