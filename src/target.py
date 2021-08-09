from base import Base


class Target(Base):
    @property
    def unique_name(self):
        return self._spec['unique_name']
    
    @property
    def properties(self):
        return self._spec.get('properties', {})

    @property
    def description(self):
        return self.properties.get('description')
    
    @property
    def runtime_user(self):
        # This is the runtime user for the target, not for the action.
        self._engine.runtime_users.get(self.properties.get('default_runtime_user_id'))
    
    @property
    def type(self):
        return self._spec.get('type', '')

    @property
    def disable_certificate_validation(self):
        return self.properties.get('disable_certificate_validation', False)

    @property
    def host(self):
        return self.properties.get('host', '')

    @property
    def path(self):
        return self.properties.get('path', '')

    @property
    def display_name(self):
        return self.properties.get('display_name', '')

    @property
    def protocol(self):
        return self.properties.get('protocol', 'https')

    @property
    def runtime_user(self):
        return self._engine.runtime_users.get(self.properties.get('default_runtime_user_id', ''))
    
    @property
    def fqdn(self):
        return f'{self.protocol}://{self.host}{self.path}'