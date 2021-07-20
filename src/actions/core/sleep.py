import time

from actions import BaseAction
from core.logger import logger

class Action(BaseAction):
    def execute(self, sleep_interval):
        logger.info(f"Sleeping for {sleep_interval} seconds")
        return time.sleep(int(sleep_interval))