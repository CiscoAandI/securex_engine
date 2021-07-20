from base import Base

class RuntimeUser(Base):
    @property
    def properties(self):
        return self._spec.get('properties', {})

    @property
    def auth_option(self):
        return self.properties.get('auth_option', '')
    
    @property
    def basic_username(self):
        return self.properties.get('basic_username', '')
    
    @property
    def basic_password(self):
        return self.properties.get('basic_password', '')
        
    def __iter__(self):
        for k, v in self._spec.items():
            if k == 'properties':
                v = {
                    **v,
                    **({
                        'basic_username': '*' * 5,
                        'basic_password': '*' * 5
                       } if v.get('auth_option') == 'Basic' else {}),
                }
            yield k, v