import importlib


class Mapper:
    @staticmethod
    def get(action):
        module = importlib.import_module(f'actions.{action}')
        if 'Action' not in dir(module):
            return Mapper.unsupported(f"Module {action} does not have Action class. Please instantiate an action class.")
        elif 'execute' not in dir(module.Action):
            return Mapper.unsupported(f"Module {action}'s Action class does not have an 'execute' function.")

        return module.Action
    
    @staticmethod
    def unsupported(message=''):
        message = message or f"Function call not supported for args: {args} and kwargs: {pprint.pformat(kwargs)}"
        def closure(*args, message=message, **kwargs):
            raise Exception(message)
        return closure