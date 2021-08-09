import os
import json
import jsonschema
from core.logger import logger

SCHEMA = "src/core/workflow_spec.json"

class Validator:
    def __init__(self, instance):
        self._draft_validator = jsonschema.Draft7Validator(json.load(open(SCHEMA)))
        self._instance = instance
    
    def validate(self):
        return [i for i in self._draft_validator.iter_errors(instance=self._instance)]


if __name__ == "__main__":
    for location, folders, files in os.walk('.'):
        for file in files:
            if file.endswith('.json'):
                file_location = os.path.join(location, file)
                errors = Validator(json.load(open(file_location))).validate()
                if errors:
                    for error in errors:
                        logger.error(error)
                    raise errors[0]
                else:
                    logger.info(f"No errors in {file_location}")