import math
import json
import re
from core.secret_retriever import SecretRetriever
import fnmatch

GLOBAL_TIMEOUT = math.inf
ATOMIC_ACTION_PATH = "SXO/Atomics/"
SUB_WORKFLOW_PATH = "SXO/Workflows/"
# Convert booleans to strings so we can compare them together for == and !=
# This is done by SXO so we should mimic this here
OPERATOR_MAP = {
    'eq': lambda x, y: str(x) == str(y),  # Equals
    'eqi': lambda x, y: str(x).casefold() == str(y).casefold(),  # Equals ignore case
    'mregex': lambda x, y: re.match(y, x) is not None,  # Matches regular expression
    'mw': lambda x, y: fnmatch.filter([x], y),  # Matches wild card
    'ne': lambda x, y: str(x) != str(y),  # Not Equal
    'and': lambda x, y: str(x).lower() == 'true' and str(y).lower() == 'true',
    'or': lambda x, y: str(x).lower() == 'true' or str(y).lower() == 'true',
}

CAST_MAP = {
    'integer': int,
    
    # For some reason the string cast in SXO turn \n into \\n and so i think it's json.dumps'ing it.
    'string': str
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
    },
    # TE API prefix
    "variable_01Q13QHPAZ0UW5fThza9uDMQqx3sOunQ9C5": {
        'global': {
            'variable_01Q13QHPAZ0UW5fThza9uDMQqx3sOunQ9C5': '/v6'
        }
    },
    "variable_01PX6MZ7OKBV91IzAIwgRSoD3Tu3qDK0gEP": {
        'global': {
            'variable_01PX6MZ7OKBV91IzAIwgRSoD3Tu3qDK0gEP': json.dumps([{
                'CustomerName': 'ACME',
                'Key': 'SysId',
                'Value': '70dfc1de1be9bcd0c1c6dd71ec4bcb62'
            }, {
                'CustomerName': 'ACME',
                'Key': 'PilotName',
                'Value': 'IaaS_Pilot_03'
            }, {
                'CustomerName': 'HPE',
                'Key': 'SysId',
                'Value': 'd93b343ddbd1f410e21ca73fd39619ff'
            }, {
                'CustomerName': 'HPE',
                'Key': 'PilotName',
                'Value': 'IaaS_Pilot_02'
            }, {
                'CustomerName': 'Unilever',
                'Key': 'SysId',
                'Value': 'c4a1bcbddb91f410e21ca73fd3961929'
            }, {
                'CustomerName': 'Unilever',
                'Key': 'PilotName',
                'Value': 'IaaS_Pilot_01'
            }])
        }
    }
}
ACCOUNT_KEYS = SecretRetriever.get_account_key()
SECURE_STRINGS = SecretRetriever.get_secure_strings()