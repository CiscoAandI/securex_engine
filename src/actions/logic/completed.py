import sys

from actions import BaseAction
from exceptions import StopEngineException


class Action(BaseAction):
    def execute(self, completion_type, result_message):
        raise StopEngineException(result_message, completion_type=completion_type)