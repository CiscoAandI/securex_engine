class StopEngineException(Exception):
    def __init__(self, *args, completion_type='completed', **kwargs):
        self.completion_type = completion_type
        return super().__init__(*args, **kwargs)