import json
import boto3
import base64
from botocore.exceptions import ClientError

class SecretRetriever:
    ACCOUNT_KEYS_NAME = 'sxo_account_keys'
    
    def get_account_key():
        return {
            k: json.loads(v)
            for k, v in json.loads(SecretRetriever._get_secret(SecretRetriever.ACCOUNT_KEYS_NAME)).items()
        }

    @staticmethod
    def _get_secret(secret_name, region_name='us-east-1'):
        # Create a Secrets Manager client
        client = boto3.session.Session().client(service_name='secretsmanager', region_name=region_name)
        
        # Can throw key error if base64 encoded
        return client.get_secret_value(SecretId=secret_name)['SecretString']

