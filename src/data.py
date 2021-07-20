import math

GLOBAL_TIMEOUT = math.inf
ATOMIC_ACTION_PATH = "objects/automation/atomic_actions/"
SUB_WORKFLOW_PATH = "objects/automation/workflows/"
# Convert booleans to strings so we can compare them together for == and !=
# This is done by SXO so we should mimic this here
OPERATOR_MAP = {
    'eq': lambda x, y: str(x) == str(y),  # Equals
    'eqi': lambda x, y: str(x).casefold() == str(y).casefold(),  # Equals ignore case
    'mregex': None,  # Matches regular expression
    'mw': None,  # Matches wild card
    'ne': lambda x, y: str(x) != str(y),  # Not Equal
    'and': lambda x, y: str(x).lower() == 'true' and str(y).lower() == 'true',
    'or': lambda x, y: str(x).lower() == 'true' or str(y).lower() == 'true',
}
GLOBALS = {
    # For some reason, SXO uses syntax that doubly-nests these
    # Example: $global.variable_01PIE3ZDEI7MP1SYSRDJrfUMisbYzIykzZN.global.variable_01PIE3ZDEI7MP1SYSRDJrfUMisbYzIykzZN$
    #
    # True
    'variable_01PIE3ZDEI7MP1SYSRDJrfUMisbYzIykzZN': {
        'global': {
            'variable_01PIE3ZDEI7MP1SYSRDJrfUMisbYzIykzZN': 'True'
        }
    },
    # Service Now Test Sys ID
    'variable_01PCUNHQ7WS0U05FLSw4WNwaGasYMJKsDHx': {
        'global': {
            'variable_01PCUNHQ7WS0U05FLSw4WNwaGasYMJKsDHx': '19dd95f4dbd5ef00e0eaaed15b961955'
        }
    }
}