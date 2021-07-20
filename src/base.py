class Base:
    def __init__(self, engine, spec):
        self._spec = spec
        self._engine = engine
    
    def __iter__(self):
        for k, v in self._spec.items():
            yield k, v