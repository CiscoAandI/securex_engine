import json
import boto3
import base64
from botocore.exceptions import ClientError

class SecretRetriever:
    ACCOUNT_KEYS_NAME = 'sxo_account_keys'
    
    def get_account_key(key_id):
        if key_id == 'definition_runtime_user_01PCLIKIUV8PP5jO3ccVGWyy4vADLPpRPsG':
            return 
        keys = json.loads(SecretRetriever._get_secret(SecretRetriever.ACCOUNT_KEYS_NAME))
        
        if key_id in keys:
            return json.loads(keys[key_id])
        else:
            raise KeyError(f"{key_id} not found. Available keys are: {', '.join(keys)}")

    @staticmethod
    def _get_secret(secret_name, region_name='us-east-1'):
        # Create a Secrets Manager client
        client = boto3.session.Session().client(service_name='secretsmanager', region_name=region_name)
        
        # Can throw key error if base64 encoded
        return client.get_secret_value(SecretId=secret_name)['SecretString']

