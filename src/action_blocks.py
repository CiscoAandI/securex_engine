from base import Base

class ActionBlocks(Base):
    # Used for conditionals, groups, loops, etc...
    @property
    def properties(self):
        return self._spec.get('properties', {})
